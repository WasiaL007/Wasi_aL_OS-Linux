#!/usr/bin/env python3

import getpass
import os
import platform
import socket
import sys

print("\n=== WASI AL OS : SYSTEM INFORMATION ===\n")

print(f"User          : {getpass.getuser()}")
print(f"Hostname      : {socket.gethostname()}")
print(f"OS            : {platform.system()}")
print(f"Release       : {platform.release()}")
print(f"Machine       : {platform.machine()}")
print(f"Architecture  : {platform.architecture()[0]}")
print(f"Processor     : {platform.processor() or 'Unknown'}")
print(f"Python        : {sys.version.split()[0]}")
print(f"Current Dir   : {os.getcwd()}")

try:
    print(f"Local IP      : {socket.gethostbyname(socket.gethostname())}")
except Exception:
    print("Local IP      : Unknown")
