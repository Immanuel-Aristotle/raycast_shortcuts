#!/opt/homebrew/bin/python3.11

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Unix2LocalTime
# @raycast.mode compact
# @raycast.packageName Utils

# Optional parameters:
# @raycast.icon 🕒

# Documentation:
# @raycast.author Immanuel-Aristotle
# @raycast.authorURL https://github.com/Immanuel-Aristotle

# @raycast.description Convert a Unix timestamp in seconds to YYYY-MM-DD_hh-mm-ss in local timezone and copy it.
#
# @raycast.argument1 { "type": "text", "placeholder": "1719200000" }

from datetime import datetime
import subprocess
import sys


def unix_timestamp_to_local_datetime(timestamp_raw: str) -> str:
    """Converts a Unix timestamp in seconds to a local datetime string."""
    timestamp_text = timestamp_raw.strip()
    if not timestamp_text:
        raise ValueError('Unix timestamp cannot be empty')

    try:
        timestamp = float(timestamp_text)
    except ValueError as error:
        raise ValueError('Unix timestamp must be a number of seconds') from error

    if abs(timestamp) >= 100_000_000_000:
        raise ValueError('Unix timestamp must be seconds, not milliseconds')

    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d_%H-%M-%S')


if len(sys.argv) != 2:
    raise SystemExit('Expected exactly one Unix timestamp argument')

formatted_datetime = unix_timestamp_to_local_datetime(sys.argv[1])

subprocess.run('pbcopy', text=True, input=formatted_datetime, check=True)

print(f'Copied to clipboard: {formatted_datetime}')
