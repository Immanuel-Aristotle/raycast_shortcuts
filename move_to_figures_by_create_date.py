#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title M2F
# @raycast.mode compact
# @raycast.packageName Utils
#
# Optional parameters:
# @raycast.icon 🖼️
#
# Documentation:
# @raycast.description Move a file into notebooks media folder grouped by exiftool Create Date.
# @raycast.author Immanuel-Aristotle
# @raycast.authorURL https://github.com/Immanuel-Aristotle
#
# @raycast.argument1 { "type": "text", "placeholder": "Input file path" }

import re
import shutil
import subprocess
import sys
from pathlib import Path

DESTINATION_ROOT = Path('/Users/veritas/notebook/media/figures')
CREATE_DATE_PATTERN = re.compile(r'Create Date\s*:\s*(\d{4}):(\d{2}):(\d{2})\b')


def get_input_path() -> Path:
    """Return the validated absolute input file path."""
    if len(sys.argv) < 2:
        print('❌ Missing input file path', file=sys.stderr)
        sys.exit(1)

    input_path = Path(sys.argv[1]).expanduser().resolve()
    if not input_path.is_file():
        print(f'❌ Input file does not exist: {input_path}', file=sys.stderr)
        sys.exit(1)

    return input_path


def get_create_date(input_path: Path) -> tuple[str, str, str]:
    """Read Create Date from exiftool and return year, month, and day."""
    try:
        result = subprocess.run(
            ['exiftool', str(input_path)],
            capture_output=True,
            text=True,
            check=True,
        )
    except FileNotFoundError:
        print('❌ exiftool is not installed or not in PATH', file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as error:
        stderr = error.stderr.strip() or error.stdout.strip() or str(error)
        print(f'❌ Failed to read metadata: {stderr}', file=sys.stderr)
        sys.exit(1)

    match = CREATE_DATE_PATTERN.search(result.stdout)
    if match is None:
        print('❌ exiftool Create Date not found or not parseable', file=sys.stderr)
        sys.exit(1)

    return match.groups()


def move_file(input_path: Path, destination_root: Path) -> Path:
    """Move the input file into the destination tree derived from Create Date."""
    year, month, day = get_create_date(input_path)
    destination_dir = destination_root / year / month / day
    destination_dir.mkdir(parents=True, exist_ok=True)

    destination_path = destination_dir / input_path.name
    if destination_path.exists():
        print(f'❌ Destination file already exists: {destination_path}', file=sys.stderr)
        sys.exit(1)

    try:
        return Path(shutil.move(str(input_path), str(destination_path)))
    except OSError as error:
        print(f'❌ Failed to move file: {error}', file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Execute the Raycast shortcut."""
    input_path = get_input_path()
    destination_path = move_file(input_path, DESTINATION_ROOT)
    print(f'Moved to: {destination_path}')


if __name__ == '__main__':
    main()
