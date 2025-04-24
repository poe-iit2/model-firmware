#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse

files = [
    "config.py",
    "device.py",
    "hilink.py",
    "led_effects.py",
    "main.py",
    "websocket.py"
]

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=str, required=False)
args = parser.parse_args()

cwd = os.path.dirname(os.path.realpath(__file__))
src = os.path.join(cwd, "../src")

subprocess.run([
    sys.executable, "-m", "mpremote",
    *(("connect", args.port) if args.port else ()),
    "fs", "cp", *(os.path.join(src, file) for file in files), ":/"
])

