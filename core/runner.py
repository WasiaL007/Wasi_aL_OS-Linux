#!/usr/bin/env python3

from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = ROOT / "reports" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    if len(sys.argv) < 2:
        print("Module path missing.")
        return 1

    module = ROOT / sys.argv[1]

    if not module.is_file():
        print(f"Module not found: {module}")
        return 1

    started = datetime.now()
    result = subprocess.run(
        [sys.executable, str(module), *sys.argv[2:]],
        cwd=ROOT,
        check=False,
    )

    log_file = LOG_DIR / f"activity_{started:%Y%m%d}.log"
    with log_file.open("a", encoding="utf-8") as log:
        log.write(
            f"{started:%Y-%m-%d %H:%M:%S} | "
            f"{module.name} | exit={result.returncode}\n"
        )

    print(f"\nExit status : {result.returncode}")
    print(f"Activity log: {log_file}")
    input("\nPress Enter to return...")

    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
