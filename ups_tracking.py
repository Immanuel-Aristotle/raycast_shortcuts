#!/opt/homebrew/bin/python3.11

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title UPS Tracking
# @raycast.mode silent
# @raycast.packageName Better Quicklinks

# Optional parameters:
# @raycast.icon 🚚

# Documentation:
# @raycast.author Immanuel-Aristotle
# @raycast.authorURL https://github.com/Immanuel-Aristotle

# @raycast.description Track a single UPS package
#
# @raycast.argument1 { "type": "text", "placeholder": "UPS Tracking #, comma separated" }

import sys, webbrowser

tracking_nums = sys.argv[1].replace(" ", "")
track_string = tracking_nums.replace(",", " ") # UPS uses spaces to separate values
tracking_url = f"https://www.ups.com/track?track=yes&trackNums={track_string}"

# Open the URL in a new browser tab (recommended for most cases)
webbrowser.open_new_tab(tracking_url)

print(f'{tracking_nums} tracking results showed!')
