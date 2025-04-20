#!/usr/bin/env python3

import esptool
import argparse
import os

fw = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../blobs/ESP32_GENERIC-20250415-v1.25.0.bin")

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=str, required=True)
args = parser.parse_args()

esptool.main([
    "--port", args.port,
    "write_flash",
    "0x1000",
    fw
])