#!/usr/bin/env python3

# @raycast.schemaVersion 1
# @raycast.title IMG2JPG
# @raycast.mode compact
# @raycast.packageName Utils
# @raycast.icon 🖼️
# @raycast.description Convert an image to JPG in /tmp, copies the path to that img to clipboard.
#
# @raycast.argument1 { "type": "text", "placeholder": "Input image path" }

"""
AGENT: Use magick convert, write a script that takes a photo input into jpg, put it into /tmp and output the abs path of the jpg file. Erase that file 1 min later.
"""


import os
import sys
import subprocess

# import time
import uuid

# --- Input ---
input_path = sys.argv[1]

if not os.path.isfile(input_path):
    print("❌ Input file does not exist")
    sys.exit(1)

# --- Output path ---
filename = f"raycast_{uuid.uuid4().hex}.jpg"
output_path = os.path.join("/tmp", filename)

# --- Convert using ImageMagick ---
try:
    subprocess.run(["magick", input_path, output_path], check=True)
except Exception as e:
    print("❌ Conversion failed:", e)
    sys.exit(1)

# --- Print absolute path ---
print(f"JPG image path copied: {output_path}")
subprocess.run(["pbcopy"], input=output_path, text=True, check=True)

# --- Background delete after 60 seconds ---
# pid = os.fork()

# if pid == 0:
#     # child process
#     time.sleep(60)
#     try:
#         if os.path.exists(output_path):
#             os.remove(output_path)
#     except:
#         pass
#     os._exit(0)
