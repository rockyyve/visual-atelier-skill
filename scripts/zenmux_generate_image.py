#!/usr/bin/env python3
"""Generate or edit one image through ZenMux and save it to disk."""

from __future__ import annotations

import argparse
import base64
import importlib.util
import json
import mimetypes
import os
import ssl
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Any


DEFAULT_BASE_URL = "https://zenmux.ai/api/v1"
DEFAULT_MODEL = "openai/gpt-image-2"
DEFAULT_SIZE = "1024x1024"
RETRYABLE_HTTP_CODES = {408, 429, 500, 502, 503, 504}


def retry_delay(attempt: int) -> float:
    return min(2 ** attempt, 8) + attempt * 0.25


def build_ssl_context() -> ssl.SSLContext | None:
    if os.environ.get("SSL_CERT_FILE") or os.environ.get("SSL_CERT_DIR"):
        return None
    if not importlib.util.find_spec("certifi"):
        return None
    import certifi

    return ssl.create_default_context(cafile=certifi.where())


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
    with urllib.request.urlopen(image_url, timeout=180, context=build_ssl_context()) as response:  # noqa: S310
        return response.read()


def read_urlopen_json(request: urllib.request.Request, timeout: int, *, attempts: int = 3) -> dict[str, Any]:
    last_error: BaseException | None = None
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=timeout, context=build_ssl_context()) as response:  # noqa: S310
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code not in RETRYABLE_HTTP_CODES or attempt == attempts - 1:
                body = exc.read().decode("utf-8", errors="replace")
                raise RuntimeError(f"HTTP {exc.code} from {request.full_url}: {body}") from exc
            last_error = exc
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            if attempt == attempts - 1:
                raise RuntimeError(f"Network error from {request.full_url}: {exc}") from exc
            last_error = exc
        time.sleep(retry_delay(attempt))
    raise RuntimeError(f"Request failed after retries: {last_error}")


def post_json(url: str, payload: dict[str, Any], api_key: str, timeout: int) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    return read_urlopen_json(request, timeout)


def post_multipart(
    url: str,
    fields: dict[str, str],
    files: list[tuple[str, Path]],
    api_key: str,
    timeout: int,
) -> dict[str, Any]:
    boundary = f"----visualatelier-{uuid.uuid4().hex}"
    body = bytearray()

    def add_line(value: str) -> None:
        body.extend(value.encode("utf-8"))
        body.extend(b"\r\n")

    for name, value in fields.items():
        add_line(f"--{boundary}")
        add_line(f'Content-Disposition: form-data; name="{name}"')
        add_line("")
        add_line(value)

    for field_name, path in files:
        mime = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        add_line(f"--{boundary}")
        add_line(f'Content-Disposition: form-data; name="{field_name}"; filename="{path.name}"')
        add_line(f"Content-Type: {mime}")
        add_line("")
        body.extend(path.read_bytes())
        body.extend(b"\r\n")
        body.extend(b"\r\n")

    add_line(f"--{boundary}--")

    request = urllib.request.Request(
        url,
        data=bytes(body),
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    return read_urlopen_json(request, timeout)


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


def is_forbidden_error(exc: Exception) -> bool:
    status_code = getattr(exc, "status_code", None)
    response = getattr(exc, "response", None)
    if status_code is None and response is not None:
        status_code = getattr(response, "status_code", None)
    message = str(exc)
    return status_code == 403 or "HTTP 403" in message or "403" in message or "Forbidden" in message or "access_denied" in message


def image_bytes_from_response(response: dict[str, Any]) -> bytes:
    image_bytes, image_url = extract_image_payload(response)
    if image_url:
        image_bytes = fetch_image_url(image_url)
    if not image_bytes:
        raise RuntimeError("ZenMux response did not contain data[0].b64_json or data[0].url")
    return image_bytes


def generate_with_rest(args: argparse.Namespace, api_key: str, prompt: str) -> bytes:
    generations_payload = {
        "model": args.model,
        "prompt": prompt,
        "n": 1,
        "size": args.size,
    }

    if args.image and not args.generation_only:
        fields = {
            "model": args.model,
            "prompt": prompt,
            "n": "1",
            "size": args.size,
        }
        files = [("image[]", image_path) for image_path in args.image]
        try:
            response = post_multipart(
                f"{args.base_url.rstrip('/')}/images/edits",
                fields,
                files,
                api_key,
                args.timeout,
            )
            return image_bytes_from_response(response)
        except Exception as exc:
            if not args.fallback_to_generation or not is_forbidden_error(exc):
                raise
            print(
                "ZenMux edits returned 403; falling back to /images/generations without uploading reference images.",
                file=sys.stderr,
            )

    response = post_json(
        f"{args.base_url.rstrip('/')}/images/generations",
        generations_payload,
        api_key,
        args.timeout,
    )
    return image_bytes_from_response(response)


def format_zenmux_error(exc: Exception) -> str:
    message = str(exc)
    if is_forbidden_error(exc):
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
    parser.add_argument("--timeout", type=int, default=int(os.environ.get("ZENMUX_TIMEOUT", "180")))
    parser.add_argument(
        "--generation-only",
        action="store_true",
        help="Use /images/generations even when --image references are provided.",
    )
    parser.add_argument(
        "--no-generation-fallback",
        action="store_false",
        dest="fallback_to_generation",
        help="Do not fall back to /images/generations when /images/edits returns 403.",
    )
    parser.set_defaults(fallback_to_generation=True)
    parser.add_argument(
        "--provider-client",
        choices=("auto", "rest", "openai"),
        default=os.environ.get("ZENMUX_PROVIDER_CLIENT", "auto"),
        help="Client implementation. auto/rest uses ZenMux REST endpoints like oil-cover; openai uses the OpenAI SDK-compatible client.",
    )
    parser.add_argument("--check", action="store_true", help="Check local ZenMux environment without making a network request.")
    args = parser.parse_args()

    api_key = os.environ.get("ZENMUX_API_KEY")
    if not api_key:
        print("ZENMUX_API_KEY is required", file=sys.stderr)
        return 2

    if args.check:
        if args.provider_client == "openai" and not importlib.util.find_spec("openai"):
            print("OpenAI SDK is required for ZenMux. Install the openai package or use imagegen.", file=sys.stderr)
            return 2
        client_note = "OpenAI SDK" if args.provider_client == "openai" else "REST client"
        print(f"ZenMux environment check passed: ZENMUX_API_KEY and {client_note} are available.")
        return 0

    if not args.out:
        print("--out is required unless --check is used", file=sys.stderr)
        return 2

    prompt = read_prompt(args)
    if args.provider_client == "openai" and not importlib.util.find_spec("openai"):
        print("OpenAI SDK is required for ZenMux. Install the openai package or use imagegen.", file=sys.stderr)
        return 2

    try:
        if args.provider_client == "openai":
            image_bytes = generate_with_openai_sdk(args, api_key, prompt)
            client_label = "openai"
        else:
            image_bytes = generate_with_rest(args, api_key, prompt)
            client_label = "rest"
    except Exception as exc:
        print(format_zenmux_error(exc), file=sys.stderr)
        return 1

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(image_bytes)
    print(f"Saved {args.out} via ZenMux {client_label}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
