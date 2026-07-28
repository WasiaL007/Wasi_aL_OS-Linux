#!/usr/bin/env python3

import socket
from urllib.parse import urlparse

target = input("Domain/Website: ").strip()

if "://" not in target:
    target = "https://" + target

u = urlparse(target)
host = u.hostname

print("\n=== WASI AL OS : OSINT ===\n")
print(f"Host      : {host}")

try:
    ip = socket.gethostbyname(host)
    print(f"IPv4      : {ip}")
except Exception:
    print("IPv4      : Unknown")

print(f"FQDN      : {socket.getfqdn(host)}")

try:
    print(f"Reverse   : {socket.gethostbyaddr(ip)[0]}")
except Exception:
    print("Reverse   : Not available")
