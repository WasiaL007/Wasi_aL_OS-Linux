#!/usr/bin/env python3

import argparse
import socket
from concurrent.futures import ThreadPoolExecutor

COMMON_PORTS = [
    20,21,22,23,25,53,80,110,111,135,139,143,
    443,445,465,587,993,995,1433,1521,3306,
    3389,5432,5900,6379,8080,8443
]

def scan(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        s.connect((host, port))
        try:
            service = socket.getservbyport(port)
        except OSError:
            service = "unknown"
        print(f"[OPEN] {port:<5} {service}")
    except Exception:
        pass
    finally:
        s.close()

def main():
    parser = argparse.ArgumentParser(description="WASI AL OS Port Scanner")
    parser.add_argument("host", nargs="?")
    args = parser.parse_args()

    host = args.host or input("Target IP/Host: ").strip()

    print(f"\nTarget : {host}\n")

    with ThreadPoolExecutor(max_workers=50) as pool:
        for port in COMMON_PORTS:
            pool.submit(scan, host, port)

if __name__ == "__main__":
    main()
