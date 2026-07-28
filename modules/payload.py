#!/usr/bin/env python3

import argparse
import base64
import binascii
import urllib.parse


def main():
    parser = argparse.ArgumentParser(description="WASI AL OS Payload Encoder")
    parser.add_argument("text", nargs="?")
    args = parser.parse_args()

    text = args.text or input("Text: ")

    print("\nEncoded Results\n")

    print("Base64")
    print(base64.b64encode(text.encode()).decode())

    print("\nHex")
    print(binascii.hexlify(text.encode()).decode())

    print("\nURL")
    print(urllib.parse.quote(text))

if __name__ == "__main__":
    main()
