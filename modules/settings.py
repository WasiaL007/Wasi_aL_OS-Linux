#!/usr/bin/env python3

import json
from pathlib import Path

CONFIG = Path("core/config.json")

DEFAULT = {
    "theme": "default",
    "timeout": 5,
    "threads": 50,
    "reports": True,
    "version": "1.7"
}

if not CONFIG.exists():
    CONFIG.parent.mkdir(exist_ok=True)
    CONFIG.write_text(json.dumps(DEFAULT, indent=4))

cfg = json.loads(CONFIG.read_text())

print("\n=== WASI AL OS SETTINGS ===\n")

for k, v in cfg.items():
    print(f"{k:10}: {v}")

print("\nConfig File:")
print(CONFIG.resolve())
