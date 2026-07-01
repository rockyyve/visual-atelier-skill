#!/usr/bin/env python3
"""Generate or edit one image through ZenMux and save it to disk."""

from __future__ import annotations

import argparse
import base64
import importlib.util
import os
import sys
import urllib.request
from pathlib import Path


DEFAULT_BASE_URL = "https://zenmux.ai/api/v1"
DEFAULT_MODEL = "openai/gpt-image-2"
DEFAULT_SIZE = "1024x1024"


def read_prompt(args: argparse.Namespace) -> str:
    if args.prompt:
        return args.prompt
    if args.prompt_file:
        return args.prompt_file.read_text(encoding="utf-8")
    raise SystemExit("Provide --prompt or --prompt-file")


def get_field(value: object, field: str) -> object:
    if isinstance(value, dict):
        return value.get(field)
    return getattr(value, field, None)


def extract_image_payload(payload: object) -> tuple[bytes | None, str | None]:
    data = get_field(payload, "data")
    if not isinstance(data, list) or not data:
        return None, None
    first = data[0]
    b64_json = get_field(first, "b64_json")
    if isinstance(b64_json, str) and b64_json:
        return base64.b64decode(b64_json), None
    image_url = get_field(first, "url")
    if isinstance(image_url, str) and image_url:
        return None, image_url
    return None, None


def fetch_image_url(image_url: str) -> bytes:
    with urllib.request.urlopen(image_url, timeout=180) as response:  # noqa: S310
        return response.read()


def build_openai_http_client() -> object | None:
    if not importlib.util.find_spec("httpx"):
        return None
    import httpx

    proxy = (
        os.environ.get("ZENMUX_PROXY")
        or os.environ.get("HTTPS_PROXY")
        or os.environ.get("https_proxy")
        or os.environ.get("HTTP_PROXY")
        or os.environ.get("http_proxy")
    )
    if proxy:
        return httpx.Client(proxy=proxy, timeout=180.0)
    return httpx.Client(trust_env=False, timeout=180.0)


def generate_with_openai_sdk(args: argparse.Namespace, api_key: str, prompt: str) -> bytes:
    from openai import OpenAI

    client = OpenAI(
        base_url=args.base_url.rstrip("/"),
        api_key=api_key,
        http_client=build_openai_http_client(),
    )
    try:
        if args.image:
            handles = []
            try:
                for image_path in args.image:
                    handles.append(image_path.open("rb"))
                result = client.images.edit(
                    model=args.model,
                    image=handles,
                    prompt=prompt,
                    size=args.size,
                )
            finally:
                for handle in handles:
                    handle.close()
        else:
            result = client.images.generate(
                model=args.model,
                prompt=prompt,
                n=1,
                size=args.size,
            )
    finally:
        client.close()

    image_bytes, image_url = extract_image_payload(result)
    if image_url:
        image_bytes = fetch_image_url(image_url)
    if not image_bytes:
        raise RuntimeError("ZenMux SDK response did not contain data[0].b64_json or data[0].url")
    return image_bytes


def format_zenmux_error(exc: Exception) -> str:
    status_code = getattr(exc, "status_code", None)
    response = getattr(exc, "response", None)
    if status_code is None and response is not None:
        status_code = getattr(response, "status_code", None)
    message = str(exc)
    if status_code == 403 or "403" in message or "Forbidden" in message:
        return (
            "ZenMux request was forbidden (403). Check ZenMux API key, account balance, "
            "model permission, and whether the model supports this image operation. "
            "Fallback to imagegen unless the user explicitly requires ZenMux. "
            f"Original error: {message}"
        )
    return message


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--image", type=Path, action="append", default=[], help="Reference image for editing; repeat for multiple images.")
    parser.add_argument("--model", default=os.environ.get("ZENMUX_IMAGE_MODEL", DEFAULT_MODEL))
    parser.add_argument("--size", default=os.environ.get("ZENMUX_IMAGE_SIZE", DEFAULT_SIZE))
    parser.add_argument("--base-url", default=os.environ.get("ZENMUX_BASE_URL", DEFAULT_BASE_URL))
    parser.add_argument(
        "--provider-client",
        choices=("auto", "openai"),
        default=os.environ.get("ZENMUX_PROVIDER_CLIENT", "auto"),
        help="Client implementation. ZenMux is OpenAI SDK-compatible; raw HTTP fallback is intentionally disabled.",
    )
    parser.add_argument("--check", action="store_true", help="Check local ZenMux environment without making a network request.")
    args = parser.parse_args()

    api_key = os.environ.get("ZENMUX_API_KEY")
    if not api_key:
        print("ZENMUX_API_KEY is required", file=sys.stderr)
        return 2

    if args.check:
        if not importlib.util.find_spec("openai"):
            print("OpenAI SDK is required for ZenMux. Install the openai package or use imagegen.", file=sys.stderr)
            return 2
        print("ZenMux environment check passed: ZENMUX_API_KEY and OpenAI SDK are available.")
        return 0

    if not args.out:
        print("--out is required unless --check is used", file=sys.stderr)
        return 2

    prompt = read_prompt(args)
    if not importlib.util.find_spec("openai"):
        print("OpenAI SDK is required for ZenMux. Install the openai package or use imagegen.", file=sys.stderr)
        return 2

    try:
        image_bytes = generate_with_openai_sdk(args, api_key, prompt)
    except Exception as exc:
        print(format_zenmux_error(exc), file=sys.stderr)
        return 1

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(image_bytes)
    print(f"Saved {args.out} via ZenMux openai")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
