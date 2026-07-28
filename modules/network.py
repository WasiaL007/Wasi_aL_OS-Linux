#!/usr/bin/env python3

from __future__ import annotations

import argparse
import ipaddress
import platform
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime


def is_allowed_network(network: ipaddress.IPv4Network) -> bool:
    return (
        network.is_private
        or network.is_loopback
        or network.is_link_local
    )


def ping_host(ip: str, timeout: int) -> tuple[str, bool]:
    system = platform.system().lower()

    if system == "windows":
        command = ["ping", "-n", "1", "-w", str(timeout * 1000), ip]
    else:
        command = ["ping", "-c", "1", "-W", str(timeout), ip]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=timeout + 2,
        )
        return ip, result.returncode == 0
    except (subprocess.TimeoutExpired, OSError):
        return ip, False


def scan_network(
    network: ipaddress.IPv4Network,
    workers: int,
    timeout: int,
) -> list[str]:
    hosts = [str(host) for host in network.hosts()]
    online_hosts: list[str] = []

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(ping_host, host, timeout): host
            for host in hosts
        }

        completed = 0
        total = len(hosts)

        for future in as_completed(futures):
            completed += 1
            ip, online = future.result()

            if online:
                online_hosts.append(ip)
                print(f"\033[1;32m[ONLINE]\033[0m {ip}")

            print(
                f"\rScanning: {completed}/{total}",
                end="",
                flush=True,
            )

    print()
    return sorted(online_hosts, key=ipaddress.ip_address)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="WASI AL OS authorised local network scanner"
    )
    parser.add_argument(
        "network",
        nargs="?",
        help="Private/local IPv4 network, example: 192.168.1.0/24",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=40,
        help="Concurrent workers (default: 40)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=1,
        help="Ping timeout in seconds (default: 1)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_arguments()

    target = args.network
    if not target:
        target = input("Enter local network (example 192.168.1.0/24): ").strip()

    try:
        network = ipaddress.ip_network(target, strict=False)
    except ValueError:
        print("\033[1;31mInvalid IPv4 network.\033[0m")
        return 1

    if not isinstance(network, ipaddress.IPv4Network):
        print("\033[1;31mOnly IPv4 is currently supported.\033[0m")
        return 1

    if not is_allowed_network(network):
        print(
            "\033[1;31mOnly private, loopback or link-local networks "
            "are permitted.\033[0m"
        )
        return 1

    if network.num_addresses > 1024:
        print("\033[1;31mMaximum supported range is 1024 addresses.\033[0m")
        return 1

    workers = max(1, min(args.workers, 100))
    timeout = max(1, min(args.timeout, 10))

    print("\n\033[1;36mWASI AL OS — NETWORK SCAN\033[0m")
    print(f"Target  : {network}")
    print(f"Started : {datetime.now():%Y-%m-%d %H:%M:%S}\n")

    online_hosts = scan_network(network, workers, timeout)

    print("\n\033[1;33mScan Summary\033[0m")
    print(f"Network      : {network}")
    print(f"Online hosts : {len(online_hosts)}")

    if not online_hosts:
        print("No responsive hosts found.")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nScan cancelled.")
        raise SystemExit(130)
