#!/usr/bin/env python3

import os
import sys
import subprocess
from pathlib import Path

VERSION = "1.7"
BASE_DIR = Path(__file__).resolve().parent
BANNER = BASE_DIR / "banner.sh"

GREEN = "\033[1;32m"
CYAN = "\033[1;36m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
RESET = "\033[0m"


def main():
    os.chdir(BASE_DIR)

    print(f"{CYAN}")
    print("============================================================")
    print("                 WASI AL OS LINUX v1.7")
    print("                  Developer: Wasi aL")
    print("============================================================")
    print(f"{RESET}")

    if not BANNER.is_file():
        print(f"{RED}[ERROR] banner.sh was not found.{RESET}")
        print(f"Expected: {BANNER}")
        sys.exit(1)

    if not os.access(BANNER, os.X_OK):
        try:
            BANNER.chmod(BANNER.stat().st_mode | 0o111)
        except OSError as exc:
            print(f"{RED}[ERROR] Cannot make banner.sh executable.{RESET}")
            print(exc)
            sys.exit(1)

    print(f"{GREEN}[✓] Starting WASI AL OS Linux v1.7...{RESET}\n")

    try:
        result = subprocess.run(
            ["bash", str(BANNER)],
            cwd=BASE_DIR,
        )
        sys.exit(result.returncode)

    except KeyboardInterrupt:
        print(f"\n{YELLOW}WASI AL OS stopped.{RESET}")
        sys.exit(130)

    except Exception as exc:
        print(f"{RED}[ERROR] Failed to start WASI AL OS.{RESET}")
        print(exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
