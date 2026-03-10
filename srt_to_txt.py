#!/opt/homebrew/bin/python3.11

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title SRT2TXT
# @raycast.mode fullOutput
# @raycast.packageName Utils

# Optional parameters:
# @raycast.icon 📝

# Documentation:
# @raycast.author Immanuel-Aristotle
# @raycast.authorURL https://github.com/Immanuel-Aristotle

# @raycast.description Converts an SRT file to a plain text file with subtitles grouped into paragraphs every `max_duration` seconds.
#
# @raycast.argument1 { "type": "text", "placeholder": ".srt file path" }
# @raycast.argument2 { "type": "text", "optional": true, "placeholder": "duration"}


import sys
import pysrt
# import argparse
import os


def srt_to_paragraphs(input_file_path, max_duration):
    """
    Converts an SRT file to a plain text file with subtitles grouped into paragraphs every `max_duration` seconds.

    :param input_file_path: Path to the input .srt file
    :param max_duration: The duration after which to split the text into a new paragraph (in seconds)
    """
    # Generate the output filename
    filename, _ = os.path.splitext(input_file_path)
    output_file_path = f"{filename}.txt"

    # Read the input SRT file
    subs = pysrt.open(input_file_path)
    paragraph = []
    current_time = 0
    all_paragraphs = []

    for sub in subs:
        # Append the subtitle text to the current paragraph
        paragraph.append(sub.text)

        # Estimate the duration of the subtitle block (in seconds)
        duration = (
            sub.duration.seconds + sub.duration.milliseconds / 1000
        )  # Duration in seconds
        current_time += duration

        # If the max_duration is reached, start a new paragraph
        if current_time >= max_duration:
            all_paragraphs.append(" ".join(paragraph))
            paragraph = []
            current_time = 0

    # If there's any leftover paragraph, append it
    if paragraph:
        all_paragraphs.append(" ".join(paragraph))

    # Write the result to the output file
    with open(output_file_path, "w", encoding="UTF8") as output_file:
        output_file.write("\n\n".join(all_paragraphs))
        output_file.write("\n")

    print(f"Converted file saved as: {output_file_path}")


def main():
    # Set up argument parsing
    # parser = argparse.ArgumentParser(description="Convert an SRT file to plain text paragraphs.")
    # parser.add_argument("input_file", help="Path to the input .srt file")
    # parser.add_argument("-d", "--duration", type=int, default=45, help="Number of seconds per paragraph (default: 45)")
    # args = parser.parse_args()

    input_path = sys.argv[1]

    input_duration = int(sys.argv[2]) if sys.argv[2] else 45
    

    # Check if the input file exists
    if not os.path.isfile(input_path):
        print(f"Error: File '{input_path}' does not exist.")
        sys.exit(1)

    # Run the conversion
    srt_to_paragraphs(input_path, input_duration)


if __name__ == "__main__":
    main()
