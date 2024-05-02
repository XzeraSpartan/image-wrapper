from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from skimage import measure
from scipy.ndimage import binary_dilation
from scipy.interpolate import splprep, splev
import xml.etree.ElementTree as ET
import base64
from io import BytesIO

def create_svg_with_text(image_path, output_svg_path, text, dilation_iterations=5, smoothing_factor=5000, font_size="24px", letter_spacing="0px", font_style="Arial"):

    image = Image.open(image_path).convert("RGBA")
    
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    data = np.array(image)

    mask = data[:, :, 3] != 0

    mask = binary_dilation(mask, iterations=dilation_iterations)


    contours = measure.find_contours(mask, 0.5)
    max_contour = max(contours, key=len)

    tck, u = splprep([max_contour[:, 1], max_contour[:, 0]], s=smoothing_factor)
    u_new = np.linspace(u.min(), u.max(), 1000)
    smooth_contour = np.array(splev(u_new, tck)).T

    svg = ET.Element('svg', width=str(image.width), height=str(image.height), xmlns="http://www.w3.org/2000/svg", xmlns_xlink="http://www.w3.org/1999/xlink")

    image_tag = ET.SubElement(svg, 'image', href="data:image/png;base64," + img_str, width=str(image.width), height=str(image.height))


    path_data = "M " + " L ".join(f"{point[0]:.1f},{point[1]:.1f}" for point in smooth_contour) + " Z"
    path_tag = ET.SubElement(svg, 'path', id="textPath", d=path_data, fill="none")


    text_tag = ET.SubElement(svg, 'text', fill="black", style=f"font-size:{font_size}; letter-spacing:{letter_spacing}; font-family:{font_style};")
    text_path_tag = ET.SubElement(text_tag, 'textPath', href="#textPath")
    text_path_tag.set("startOffset", "0%")
    text_path_tag.text = text


    tree = ET.ElementTree(svg)
    tree.write(output_svg_path)


    plt.imshow(mask, cmap='gray')
    plt.plot(smooth_contour[:, 0], smooth_contour[:, 1], linewidth=2, color='red')
    plt.title('Smoothed and Dilated Contour with Text')
    plt.axis('off')
    plt.show()

image_path = 'image.png'  
output_svg_path = 'output.svg'  
text = "TIMOTHEE CHALAMET " * 5 
font_size = "40px"  
letter_spacing = "10px"  
font_style = "Roboto" 

create_svg_with_text(image_path, output_svg_path, text, font_size=font_size, letter_spacing=letter_spacing, font_style=font_style)
