#!/opt/homebrew/bin/python3.11

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Calculate Yaw
# @raycast.mode compact
# @raycast.packageName Utils

# Optional parameters:
# @raycast.icon 📐

# Documentation:
# @raycast.author Immanuel-Aristotle
# @raycast.authorURL https://github.com/Immanuel-Aristotle

# @raycast.description Calculate yaw (PoseHeadingDegrees) for Mapillary's true-north-centered view.  Args:      x_pixel: Subject's horizontal pixel position (0 to width-1).      image_width: Total width of the panorama.      target_bearing: Desired compass angle (0-360°) for the subject.

# @raycast.argument1 { "type": "text", "placeholder": "x pixel" }
# @raycast.argument2 { "type": "text", "placeholder": "image width" }
# @raycast.argument3 { "type": "text", "placeholder": "target bearing" }


import sys, subprocess


def calculate_yaw(x_pixel_param: int, image_width_param: int, target_bearing_param: float) -> float:
    """
    Calculate yaw (PoseHeadingDegrees) for Mapillary's true-north-centered view.

    Args:
        x_pixel_param: Subject's horizontal pixel position (0 to width-1).
        image_width: Total width of the panorama.
        target_bearing: Desired compass angle (0-360°) for the subject.

    Returns:
        Yaw angle (0-360°) to write into XMP-GPano:PoseHeadingDegrees.
    """
    center_pixel = image_width_param / 2
    offset_deg = ((x_pixel_param - center_pixel) / image_width_param) * 360.0
    calculated_yaw = (target_bearing_param - offset_deg) % 360.0
    return calculated_yaw


x_pixel, image_width, target_bearing = (
    int(sys.argv[1]),
    int(sys.argv[2]),
    float(sys.argv[3]),
)

# Your input data
# x_pixel = 7580
# image_width = 16122
# target_bearing = 59.35
# Subject should point to 59.35° on the compass

# Calculate yaw
yaw = calculate_yaw(x_pixel, image_width, target_bearing)
subprocess.run("pbcopy", text=True, input=str(yaw), check=True)

print(
    f"Pixel offset from center: {((x_pixel - image_width/2) / image_width * 360):.2f}°"
)
print(f"Required yaw (PoseHeadingDegrees): {yaw:.2f}°")
