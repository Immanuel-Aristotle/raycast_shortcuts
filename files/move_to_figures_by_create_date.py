#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Move2Figures
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
# @raycast.argument1 { "type": "text", "placeholder": "Input file or directory path" }

import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

DESTINATION_ROOT = Path('/Users/veritas/notebook/media/figures')
CREATE_DATE_PATTERN = re.compile(r'Create Date\s*:\s*(\d{4}):(\d{2}):(\d{2})\b')


def get_input_path() -> Path:
    """Return the validated absolute input path."""
    if len(sys.argv) < 2:
        print('❌ Missing input file or directory path', file=sys.stderr)
        sys.exit(1)

    input_path = Path(sys.argv[1]).expanduser().resolve()
    if not input_path.exists():
        print(f'❌ Input path does not exist: {input_path}', file=sys.stderr)
        sys.exit(1)

    return input_path


class MoveError(Exception):
    """Raised when a file cannot be moved into the figures tree."""


@dataclass
class BatchResult:
    """Summary of a directory batch move."""

    moved_paths: list[Path]
    failures: list[tuple[Path, str]]
    skipped_non_images: int
    image_file_count: int


def get_mime_type(input_path: Path) -> str:
    """Return the MIME type detected by the system file command."""
    try:
        result = subprocess.run(
            ['file', '--brief', '--mime-type', str(input_path)],
            capture_output=True,
            text=True,
            check=True,
        )
    except FileNotFoundError as error:
        raise MoveError('file command is not available') from error
    except subprocess.CalledProcessError as error:
        stderr = error.stderr.strip() or error.stdout.strip() or str(error)
        raise MoveError(f'Failed to detect MIME type: {stderr}') from error

    mime_type = result.stdout.strip()
    if not mime_type:
        raise MoveError('Failed to detect MIME type: empty output from file')

    return mime_type


def ensure_image_file(input_path: Path) -> None:
    """Ensure the path points to an image according to MIME type."""
    mime_type = get_mime_type(input_path)
    if not mime_type.startswith('image/'):
        raise MoveError(f'Not an image file (MIME: {mime_type})')


def get_create_date(input_path: Path) -> tuple[str, str, str]:
    """Read Create Date from exiftool and return year, month, and day."""
    try:
        result = subprocess.run(
            ['exiftool', str(input_path)],
            capture_output=True,
            text=True,
            check=True,
        )
    except FileNotFoundError as error:
        raise MoveError('exiftool is not installed or not in PATH') from error
    except subprocess.CalledProcessError as error:
        stderr = error.stderr.strip() or error.stdout.strip() or str(error)
        raise MoveError(f'Failed to read metadata: {stderr}') from error

    match = CREATE_DATE_PATTERN.search(result.stdout)
    if match is None:
        raise MoveError('exiftool Create Date not found or not parseable')

    return match.groups()


def move_file(input_path: Path, destination_root: Path) -> Path:
    """Move the input file into the destination tree derived from Create Date."""
    ensure_image_file(input_path)
    year, month, day = get_create_date(input_path)
    destination_dir = destination_root / year / month / day
    destination_dir.mkdir(parents=True, exist_ok=True)

    destination_path = destination_dir / input_path.name
    if destination_path.exists():
        raise MoveError(f'Destination file already exists: {destination_path}')

    try:
        return Path(shutil.move(str(input_path), str(destination_path)))
    except OSError as error:
        raise MoveError(f'Failed to move file: {error}') from error


def move_directory(input_dir: Path, destination_root: Path) -> BatchResult:
    """Move each first-level image file in the directory into the figures tree."""
    moved_paths: list[Path] = []
    failures: list[tuple[Path, str]] = []
    skipped_non_images = 0
    image_file_count = 0

    for child in sorted(input_dir.iterdir()):
        if not child.is_file():
            continue

        try:
            mime_type = get_mime_type(child)
        except MoveError as error:
            failures.append((child, str(error)))
            continue

        if not mime_type.startswith('image/'):
            skipped_non_images += 1
            continue

        image_file_count += 1

        try:
            moved_paths.append(move_file(child, destination_root))
        except MoveError as error:
            failures.append((child, str(error)))

    return BatchResult(
        moved_paths=moved_paths,
        failures=failures,
        skipped_non_images=skipped_non_images,
        image_file_count=image_file_count,
    )


def format_batch_summary(result: BatchResult) -> str:
    """Return a readable directory-mode summary."""
    lines = [
        f'Moved: {len(result.moved_paths)}',
        f'Failed: {len(result.failures)}',
        f'Skipped non-images: {result.skipped_non_images}',
    ]

    if result.moved_paths:
        lines.append('')
        lines.append('Moved files:')
        lines.extend(f'- {path}' for path in result.moved_paths)

    if result.failures:
        lines.append('')
        lines.append('Failures:')
        lines.extend(f'- {path.name}: {reason}' for path, reason in result.failures)

    return '\n'.join(lines)


def main() -> None:
    """Execute the Raycast shortcut."""
    input_path = get_input_path()

    if input_path.is_file():
        try:
            destination_path = move_file(input_path, DESTINATION_ROOT)
        except MoveError as error:
            print(f'❌ {error}', file=sys.stderr)
            sys.exit(1)

        print(f'Moved to: {destination_path}')
        return

    if not input_path.is_dir():
        print(f'❌ Input path is neither a file nor a directory: {input_path}', file=sys.stderr)
        sys.exit(1)

    result = move_directory(input_path, DESTINATION_ROOT)
    if result.image_file_count == 0:
        print(f'❌ No image files found in directory: {input_path}', file=sys.stderr)
        sys.exit(1)

    output = format_batch_summary(result)
    if result.failures:
        print(output, file=sys.stderr)
        sys.exit(1)

    print(output)


if __name__ == '__main__':
    main()
