#!/usr/bin/env python3

import json
from pathlib import Path

CONFIG = Path("core/config.json")

THEMES = {
    "1": "default",
    "2": "blue",
    "3": "green",
    "4": "red",
    "5": "purple"
}

cfg = json.loads(CONFIG.read_text())

print("\n=== WASI AL OS THEME MANAGER ===\n")

for k, v in THEMES.items():
    print(f"{k}. {v}")

choice = input("\nSelect theme: ").strip()

if choice in THEMES:
    cfg["theme"] = THEMES[choice]
    CONFIG.write_text(json.dumps(cfg, indent=4))
    print(f"\nTheme changed to: {THEMES[choice]}")
else:
    print("\nInvalid option.")
