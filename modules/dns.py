#!/usr/bin/env python3

import argparse
import socket
import sys
from pathlib import Path

SCRIPT_DIR = str(Path(__file__).resolve().parent)
if SCRIPT_DIR in sys.path:
    sys.path.remove(SCRIPT_DIR)

try:
    import dns.resolver
except ImportError:
    print("Install dependency first:")
    print("pkg install python")
    print("pip install dnspython")
    raise SystemExit(1)

RECORDS = ["A", "AAAA", "MX", "NS", "TXT", "CNAME"]

RESOLVER = dns.resolver.Resolver(configure=False)
RESOLVER.nameservers = ["1.1.1.1", "8.8.8.8"]
RESOLVER.timeout = 3
RESOLVER.lifetime = 5


def lookup(domain):
    print(f"\nTarget : {domain}\n")

    try:
        print("IP Address")
        print(socket.gethostbyname(domain))
    except Exception:
        print("Unavailable")

    for record in RECORDS:
        print(f"\n[{record}]")
        try:
            answers = RESOLVER.resolve(domain, record)
            for item in answers:
                print(item.to_text())
        except Exception:
            print("No record")


def main():
    parser = argparse.ArgumentParser(
        description="WASI AL OS DNS Toolkit"
    )
    parser.add_argument("domain", nargs="?")
    args = parser.parse_args()

    target = args.domain or input("Domain: ").strip()

    lookup(target)


if __name__ == "__main__":
    main()
