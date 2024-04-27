from PIL import Image

# Load the image with transparency
image_path = 'no-bg-1714097572343.png'
image = Image.open(image_path)
image = image.convert("RGBA")  # Ensure it's in RGBA format

# Prepare to mark the image
marked_image = image.copy()
pixels = marked_image.load()

width, height = image.size

# Process each row
for y in range(height):
    last_pixel_was_transparent = True
    left_transitions = []
    right_transitions = []

    # Scan left to right
    for x in range(width):
        r, g, b, a = pixels[x, y]
        if a != 0:  # This pixel is not transparent
            if last_pixel_was_transparent:
                left_transitions.append(x)  # Mark the transition point
            last_pixel_was_transparent = False
        else:
            last_pixel_was_transparent = True
    
    # Scan right to left
    last_pixel_was_transparent = True
    for x in range(width-1, -1, -1):
        r, g, b, a = pixels[x, y]
        if a != 0:  # This pixel is not transparent
            if last_pixel_was_transparent:
                right_transitions.append(x)  # Mark the transition point
            last_pixel_was_transparent = False
        else:
            last_pixel_was_transparent = True

    # Combine transitions and mark them in red
    for x in left_transitions:
        pixels[x, y] = (255, 0, 0, 255)  # Red color
    for x in right_transitions:
        pixels[x, y] = (255, 0, 0, 255)  # Red color

# Save or show the image
marked_image.show()
