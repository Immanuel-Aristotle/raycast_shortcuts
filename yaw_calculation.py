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

def calculate_yaw(x_pixel: int, image_width: int, target_bearing: float) -> float:
    """
    Calculate yaw (PoseHeadingDegrees) for Mapillary's true-north-centered view.
    
    Args:
        x_pixel: Subject's horizontal pixel position (0 to width-1).
        image_width: Total width of the panorama.
        target_bearing: Desired compass angle (0-360°) for the subject.
    
    Returns:
        Yaw angle (0-360°) to write into XMP-GPano:PoseHeadingDegrees.
    """
    center_pixel = image_width / 2
    offset_deg = ((x_pixel - center_pixel) / image_width) * 360.0
    yaw = (target_bearing - offset_deg) % 360.0
    return yaw


x_pixel, image_width, target_bearing = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])

# Your input data
# x_pixel = 7580
# image_width = 16122
# target_bearing = 59.35  
# Subject should point to 59.35° on the compass

# Calculate yaw
yaw = calculate_yaw(x_pixel, image_width, target_bearing)
subprocess.run("pbcopy", text=True, input=str(yaw))

print(f"Pixel offset from center: {((x_pixel - image_width/2) / image_width * 360):.2f}°")
print(f"Required yaw (PoseHeadingDegrees): {yaw:.2f}°")
