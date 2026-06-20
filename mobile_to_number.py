#!/opt/homebrew/bin/python3.11

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Mobile2Number
# @raycast.mode silent
# @raycast.packageName Utils

# Optional parameters:
# @raycast.icon 🔢

# Documentation:
# @raycast.author Immanuel-Aristotle
# @raycast.authorURL https://github.com/Immanuel-Aristotle

# @raycast.description Convert a formatted phone number to digits only
#
# @raycast.argument1 { "type": "text", "placeholder": "+1 (217) 333-1100" }

import re
import subprocess
import sys

ALLOWED_PHONE_PATTERN = re.compile(r'^[\d\s()+-]+$')


def phone_to_digits(phone_number: str) -> str:
    """Converts a formatted phone number into digits only."""
    if not phone_number:
        raise ValueError('Phone number cannot be empty')

    if not ALLOWED_PHONE_PATTERN.fullmatch(phone_number):
        raise ValueError('Phone number contains unsupported characters')

    digits = ''.join(character for character in phone_number if character.isdigit())
    if not digits:
        raise ValueError('Phone number must contain at least one digit')

    return digits


if len(sys.argv) != 2:
    raise SystemExit('Expected exactly one phone number argument')

converted_number = phone_to_digits(sys.argv[1])

subprocess.run('pbcopy', text=True, input=converted_number, check=True)

print(f'Copied to clipboard: {converted_number}')
