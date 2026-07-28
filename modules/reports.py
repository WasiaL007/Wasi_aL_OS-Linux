#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path

REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)

report = REPORT_DIR / f"report_{datetime.now():%Y%m%d_%H%M%S}.txt"

with report.open("w", encoding="utf-8") as f:
    f.write("WASI AL OS REPORT\n")
    f.write("=" * 40 + "\n")
    f.write(f"Generated : {datetime.now()}\n")
    f.write("Status    : Success\n")

print("\nReport created:")
print(report.resolve())
