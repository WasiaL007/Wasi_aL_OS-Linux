#!/usr/bin/env python3

import shutil
import platform
import subprocess
from pathlib import Path

print("\n=== WASI AL OS : SYSTEM STATUS ===\n")

usage = shutil.disk_usage(Path.home())

print(f"OS           : {platform.system()} {platform.release()}")
print(f"Architecture : {platform.machine()}")
print(f"Total Space  : {usage.total // (1024**3)} GB")
print(f"Used Space   : {usage.used // (1024**3)} GB")
print(f"Free Space   : {usage.free // (1024**3)} GB")

try:
    print("\nMemory:")
    subprocess.run(["free", "-h"], check=False)
except FileNotFoundError:
    print("Memory information not available.")

try:
    print("\nUptime:")
    subprocess.run(["uptime"], check=False)
except FileNotFoundError:
    print("Uptime information not available.")
