#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title OFD
# @raycast.mode compact
# @raycast.packageName Utils
#
# Optional parameters:
# @raycast.icon 📂
#
# Documentation:
# @raycast.description Open ~/notebook/media/figures/YYYY/MM/DD in Finder.
# @raycast.author Immanuel-Aristotle
# @raycast.authorURL https://github.com/Immanuel-Aristotle
#
# @raycast.argument1 { "type": "text", "optional": true, "placeholder": "YYYY (blank = today)" }
# @raycast.argument2 { "type": "text", "optional": true, "placeholder": "MM (blank = today)" }
# @raycast.argument3 { "type": "text", "optional": true, "placeholder": "DD (blank = today)" }

import subprocess
import sys
from datetime import date
from pathlib import Path

DESTINATION_ROOT = Path.home() / 'notebook' / 'media' / 'figures'


def get_argument(index: int) -> str:
    """Return a trimmed CLI argument or an empty string when absent."""
    if len(sys.argv) <= index:
        return ''
    return sys.argv[index].strip()


def parse_date_parts() -> tuple[str, str, str]:
    """Resolve year, month, and day from args, defaulting blanks to today."""
    today = date.today()

    year_raw = get_argument(1)
    month_raw = get_argument(2)
    day_raw = get_argument(3)

    year = year_raw or f'{today.year:04d}'
    month = month_raw or f'{today.month:02d}'
    day = day_raw or f'{today.day:02d}'

    if not (year.isdigit() and len(year) == 4):
        print(f'❌ Invalid year: {year}', file=sys.stderr)
        sys.exit(1)

    if not month.isdigit():
        print(f'❌ Invalid month: {month}', file=sys.stderr)
        sys.exit(1)

    if not day.isdigit():
        print(f'❌ Invalid day: {day}', file=sys.stderr)
        sys.exit(1)

    month_value = int(month)
    day_value = int(day)

    if not 1 <= month_value <= 12:
        print(f'❌ Month must be between 1 and 12: {month}', file=sys.stderr)
        sys.exit(1)

    if not 1 <= day_value <= 31:
        print(f'❌ Day must be between 1 and 31: {day}', file=sys.stderr)
        sys.exit(1)

    return year, f'{month_value:02d}', f'{day_value:02d}'


def open_directory(target_dir: Path) -> None:
    """Create and open the target directory in Finder."""
    target_dir.mkdir(parents=True, exist_ok=True)

    try:
        subprocess.run(['open', str(target_dir)], check=True)
    except FileNotFoundError:
        print('❌ open command is not available', file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as error:
        print(f'❌ Failed to open directory: {error}', file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Execute the Raycast shortcut."""
    year, month, day = parse_date_parts()
    target_dir = DESTINATION_ROOT / year / month / day
    open_directory(target_dir)
    print(f'Opened: {target_dir}')


if __name__ == '__main__':
    main()
