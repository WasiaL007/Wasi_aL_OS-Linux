#!/usr/bin/env python3

import argparse
import hashlib

ALGORITHMS = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha224": hashlib.sha224,
    "sha256": hashlib.sha256,
    "sha384": hashlib.sha384,
    "sha512": hashlib.sha512,
}

def main():
    parser = argparse.ArgumentParser(description="WASI AL OS Hash Toolkit")
    parser.add_argument("text", nargs="?")
    args = parser.parse_args()

    text = args.text or input("Text: ")
    data = text.encode()

    print("\nHash Results\n")

    for name, func in ALGORITHMS.items():
        print(f"{name.upper():8} : {func(data).hexdigest()}")

if __name__ == "__main__":
    main()
