#!/opt/homebrew/bin/python3.11

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Copy SMS Code
# @raycast.mode compact
# @raycast.packageName Messages
#
# Optional parameters:
# @raycast.icon 💬
#
# Documentation:
# @raycast.description Copy verification code from a message in 10 minutes.
# @raycast.author Immanuel-Aristotle
# @raycast.authorURL https://github.com/Immanuel-Aristotle

import sqlite3
import re
import subprocess

# --- Configuration ---
username = "veritas"
TIME_WINDOW_SECONDS = 600
KEYWORDS = ["验证码", "code", "验证代码"]

db_path = f"/Users/{username}/Library/Messages/chat.db"

# --- SQL: get ALL messages in time window ---
query = f"""
SELECT
  datetime(date/1000000000 + 978307200, 'unixepoch', 'localtime') AS time,
  text
FROM message
WHERE
  text IS NOT NULL
  AND datetime(date/1000000000 + 978307200, 'unixepoch', 'localtime')
      > datetime('now', 'localtime', '-{TIME_WINDOW_SECONDS} second')
ORDER BY date DESC;
"""

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute(query)

# rows now contains ALL messages in TIME_WINDOW_SECONDS
rows = cursor.fetchall()
conn.close()

if not rows:
    print(f"No messages in the past {TIME_WINDOW_SECONDS} seconds.")
    raise SystemExit(0)

# --- Regex preparation ---
keyword_pattern = re.compile("|".join(KEYWORDS), re.IGNORECASE)
code_pattern = re.compile(r"\b\d{4,6}\b")

codes_found = []

# Iterate messages in chronological order (older → newer)
for _, text in reversed(rows):
    if not keyword_pattern.search(text):
        continue

    matches = code_pattern.findall(text)
    if matches:
        codes_found.extend(matches)

if not codes_found:
    print(f"No verification code found in the past {TIME_WINDOW_SECONDS} seconds")
    raise SystemExit(0)

# --- Take the FIRST verification code ---
code = codes_found[-1]

# Copy to clipboard
subprocess.run("pbcopy", text=True, input=code, check=True)

print(f"{code} code copied!")
