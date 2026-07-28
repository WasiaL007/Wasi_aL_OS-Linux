#!/usr/bin/env python3

from __future__ import annotations

import argparse
import socket
import ssl
import sys
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

SECURITY_HEADERS = {
    "strict-transport-security": "HSTS",
    "content-security-policy": "Content-Security-Policy",
    "x-content-type-options": "X-Content-Type-Options",
    "x-frame-options": "X-Frame-Options",
    "referrer-policy": "Referrer-Policy",
    "permissions-policy": "Permissions-Policy",
}


def normalise_url(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("URL cannot be empty.")
    if "://" not in value:
        value = "https://" + value
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Enter a valid HTTP or HTTPS URL.")
    return value


def fetch_target(url: str, timeout: int) -> tuple[int, str, dict[str, str]]:
    request = Request(
        url,
        headers={
            "User-Agent": "WASI-AL-OS-Web-Scanner/1.7",
            "Accept": "*/*",
        },
        method="GET",
    )

    try:
        with urlopen(request, timeout=timeout) as response:
            headers = {key.lower(): value for key, value in response.headers.items()}
            return response.status, response.geturl(), headers
    except HTTPError as error:
        headers = {key.lower(): value for key, value in error.headers.items()}
        return error.code, error.geturl(), headers


def inspect_tls(hostname: str, port: int, timeout: int) -> dict[str, str]:
    context = ssl.create_default_context()

    with socket.create_connection((hostname, port), timeout=timeout) as connection:
        with context.wrap_socket(connection, server_hostname=hostname) as secure_socket:
            certificate = secure_socket.getpeercert()
            cipher = secure_socket.cipher()

    expiry_raw = certificate.get("notAfter", "")
    expiry_text = "Unknown"
    days_left = "Unknown"

    if expiry_raw:
        expiry = datetime.strptime(
            expiry_raw,
            "%b %d %H:%M:%S %Y %Z",
        ).replace(tzinfo=timezone.utc)
        expiry_text = expiry.strftime("%Y-%m-%d %H:%M:%S UTC")
        days_left = str((expiry - datetime.now(timezone.utc)).days)

    return {
        "protocol": secure_socket.version() or "Unknown",
        "cipher": cipher[0] if cipher else "Unknown",
        "expires": expiry_text,
        "days_left": days_left,
    }


def print_header_report(headers: dict[str, str]) -> None:
    print("\nSecurity Headers")

    for header, label in SECURITY_HEADERS.items():
        if header in headers:
            print(f"\033[1;32m[FOUND]\033[0m   {label}")
        else:
            print(f"\033[1;33m[MISSING]\033[0m {label}")

    server = headers.get("server", "Not disclosed")
    powered_by = headers.get("x-powered-by", "Not disclosed")

    print("\nInformation Disclosure")
    print(f"Server       : {server}")
    print(f"X-Powered-By : {powered_by}")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="WASI AL OS authorised web security scanner"
    )
    parser.add_argument("url", nargs="?", help="Website URL")
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Connection timeout in seconds",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_arguments()
    target = args.url or input("Enter authorised website URL: ")

    try:
        url = normalise_url(target)
    except ValueError as error:
        print(f"\033[1;31m{error}\033[0m")
        return 1

    timeout = max(1, min(args.timeout, 30))
    parsed = urlparse(url)

    print("\n\033[1;36mWASI AL OS — WEB SCANNER\033[0m")
    print(f"Target  : {url}")
    print(f"Started : {datetime.now():%Y-%m-%d %H:%M:%S}")

    try:
        status, final_url, headers = fetch_target(url, timeout)
    except (URLError, TimeoutError, socket.timeout, OSError) as error:
        print(f"\n\033[1;31mConnection failed: {error}\033[0m")
        return 1

    print("\nHTTP Result")
    print(f"Status    : {status}")
    print(f"Final URL : {final_url}")

    print_header_report(headers)

    if parsed.scheme == "https" and parsed.hostname:
        print("\nTLS Information")
        try:
            tls = inspect_tls(parsed.hostname, parsed.port or 443, timeout)
            print(f"Protocol  : {tls['protocol']}")
            print(f"Cipher    : {tls['cipher']}")
            print(f"Expires   : {tls['expires']}")
            print(f"Days left : {tls['days_left']}")
        except (ssl.SSLError, socket.timeout, OSError) as error:
            print(f"\033[1;31mTLS inspection failed: {error}\033[0m")

    print("\n\033[1;33mUse only on websites you own or have permission to test.\033[0m")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nScan cancelled.")
        raise SystemExit(130)
