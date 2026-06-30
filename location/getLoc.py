#!/opt/homebrew/bin/python3.11

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title GetLoc
# @raycast.mode silent
# @raycast.packageName Utils

# Optional parameters:
# @raycast.icon 📌

# Documentation:
# @raycast.author Immanuel-Aristotle
# @raycast.authorURL https://github.com/Immanuel-Aristotle

# @raycast.description Getting current location

import subprocess

loc = subprocess.run("corelocationcli", text=True, check=True, capture_output=True)

subprocess.run("pbcopy", text=True, input=loc.stdout, check=True)

print(f"\n📋 Copied to clipboard: {loc.stdout}")
