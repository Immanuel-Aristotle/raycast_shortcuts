#!/opt/homebrew/bin/python3.11

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Delete Whitespaces
# @raycast.mode silent
# @raycast.packageName Utils

# Optional parameters:
# @raycast.icon ✂️

# Documentation:
# @raycast.author Immanuel-Aristotle
# @raycast.authorURL https://github.com/Immanuel-Aristotle

# @raycast.description Eliminating all whitespaces in the string
#
# @raycast.argument1 { "type": "text", "placeholder": "Delete whitespaces from..." }

import subprocess
import sys

input_str = sys.argv[1]

trimmed = input_str.replace(" ", "")

subprocess.run("pbcopy", text=True, input=trimmed, check=True)

print(f"\n📋 Copied to clipboard: {trimmed}")
