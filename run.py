#!/usr/bin/env python3

import subprocess
import sys

MENU = {
    "1": ("Information Toolkit", "modules/information.py"),
    "2": ("Network Scanner", "modules/network.py"),
    "3": ("Web Scanner", "modules/web.py"),
    "4": ("DNS Toolkit", "modules/dns.py"),
    "5": ("Port Scanner", "modules/port.py"),
    "6": ("Hash Toolkit", "modules/hash.py"),
    "7": ("Payload Encoder", "modules/payload.py"),
    "8": ("OSINT Toolkit", "modules/osint.py"),
    "9": ("Reports Toolkit", "modules/reports.py"),
    "10": ("Settings Toolkit", "modules/settings.py"),
    "11": ("Theme Manager", "modules/themes.py"),
    "12": ("System Toolkit", "modules/system.py"),
    "0": ("Exit", None),
}

while True:
    print("\n===== WASI AL OS v1.7 =====\n")
    for k, v in MENU.items():
        print(f"{k:>2}. {v[0]}")

    choice = input("\nSelect: ").strip()

    if choice == "0":
        sys.exit(0)

    if choice not in MENU:
        print("Invalid option.")
        continue

    print()
    subprocess.run([sys.executable, MENU[choice][1]])
    input("\nPress Enter to return...")
