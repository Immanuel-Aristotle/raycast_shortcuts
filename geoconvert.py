#!/opt/homebrew/bin/python3.11

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Geo Convert
# @raycast.mode compact
# @raycast.packageName Utils

# Optional parameters:
# @raycast.icon 🌐

# Documentation:
# @raycast.author Immanuel-Aristotle
# @raycast.authorURL https://github.com/Immanuel-Aristotle

# @raycast.description Convert various DMS formats (like exiftool geolocation output) into decimal degrees and copy result
#
# @raycast.argument1 { "type": "text", "placeholder": "40 deg 6' 16.56\" N, 88 deg 13'14.16\" W" }

import re
import sys
import subprocess

# Clean up input
input_str = (
    sys.argv[1]
    .replace(" ", "")
    .replace(",", "")
    .replace("deg", "°")     # Convert "deg" → "°"
)

# New powerful regex that accepts degrees symbol OR "deg"
DMS_PATTERN = re.compile(
    r"""(?P<deg>\d+)(?:°)?      # degrees
        (?P<min>\d+)[\'’]?      # minutes
        (?P<sec>\d+(\.\d+)?)["”]? # seconds
        (?P<dir>[NnSsEeWw])     # direction
    """,
    re.VERBOSE
)

matches = DMS_PATTERN.findall(input_str)

if len(matches) != 2:
    print("❌ Unable to parse two coordinates from input.")
    print("Input received:", input_str)
    sys.exit(1)

def dms_to_decimal(m):
    deg = float(m[0])
    minute = float(m[1])
    sec = float(m[2])
    direction = m[4].upper()

    dec = deg + minute/60 + sec/3600

    if direction in ("S", "W"):
        dec = -dec
    return dec

lat_dec = dms_to_decimal(matches[0])
lon_dec = dms_to_decimal(matches[1])

gmaps_format = f"{lat_dec}, {lon_dec}"

# copy to clipboard
subprocess.run("pbcopy", text=True, input=gmaps_format)

print("Latitude :", lat_dec)
print("Longitude:", lon_dec)
print("\n📋 Copied to clipboard:")
print(gmaps_format)
