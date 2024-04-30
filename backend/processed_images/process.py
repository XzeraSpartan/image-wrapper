from PIL import Image
import numpy as np
from scipy.interpolate import splprep, splev

def smooth_points_spline(points, s=3, skip=10):
    """ Generate smoother path commands using spline curves with skipping """
    if len(points) < 3:
        return []  # Not enough points to smooth
    # Reduce the number of points by skipping
    points = np.array(points[::skip])
    tck, u = splprep([points[:, 0], points[:, 1]], s=s)  # Fit spline to reduced points
    unew = np.linspace(0, 1, num=1000)  # Increase the number of points for smoothness
    out = splev(unew, tck)
    path_commands = ["M {} {}".format(out[0][0], out[1][0])]  # Move to the first point
    path_commands += ["L {} {}".format(x, y) for x, y in zip(out[0], out[1])]  # Line to each point
    return path_commands

# Load the image with transparency
image_path = 'no-bg-1714097572343.png'
image = Image.open(image_path)
image = image.convert("RGBA")  # Ensure it's in RGBA format

width, height = image.size
pixels = image.load()

# Collect edge points
left_edges = []
right_edges = []
for y in range(height):
    left_found = None
    right_found = None
    for x in range(width):
        _, _, _, a = pixels[x, y]
        if a != 0:  # This pixel is not transparent
            if left_found is None:
                left_found = (x, y)
            right_found = (x, y)  # Update right_found to the last non-transparent pixel

    if left_found:
        left_edges.append(left_found)
    if right_found:
        right_edges.append(right_found)

# Reverse the right edges for proper path continuity
right_edges.reverse()
#left_edges.reverse()
# Smooth both edge lists with a skipping value
left_path = smooth_points_spline(left_edges, s=2, skip=10)  # Adjust `s` and `skip` as needed
right_path = smooth_points_spline(right_edges, s=2, skip=10)

# Create the SVG path commands, combining both smoothed paths
svg_path = " ".join(left_path + right_path)

# Create the SVG output
svg_output = f'''
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
    <path id="myPath" d="{svg_path}" fill="none" stroke="black" stroke-linecap="round" stroke-linejoin="round"/>
    <text fill="red" font-size="65" font-family="Arial" dominant-baseline="hanging" text-anchor="start" letter-spacing="36px">
        <textPath href="#myPath" startOffset="20%" dy="10">
           Timothee Chalamet Dune Two
        </textPath>
    </text>
</svg>
'''

# Save to a file or output as needed
with open('output.svg', 'w') as f:
    f.write(svg_output)
