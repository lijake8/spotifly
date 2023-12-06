album_img_url = "https://artwork.espncdn.com/categories/394dad60-8a1a-31a8-912c-a207555bc939/1x1Feature/1440_20230418135718.jpg"

# faster
from PIL import Image
from collections import Counter
import requests
from io import BytesIO

def extract_main_colors_from_url(image_url):
    # Download the image from the URL
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))

    # Resize the image for faster processing if needed
    img = img.resize((100, 100))

    # Convert the image to RGB mode
    img = img.convert("RGB")

    # Get the pixel colors
    pixels = list(img.getdata())

    # Count the occurrences of each color
    color_counts = Counter(pixels)

    # Get the two most common colors
    main_colors = color_counts.most_common(2)

    # Extract RGB values
    main_colors_rgb = [(color[0][0], color[0][1], color[0][2]) for color in main_colors]

    return main_colors_rgb

# Example usage:
image_url = "https://m.media-amazon.com/images/I/51844EHPQoL._UF1000,1000_QL80_.jpg"
main_colors = extract_main_colors_from_url(image_url)

print("Main Colors:", main_colors)


# from colorthief import ColorThief
# import requests
# from io import BytesIO

# def extract_main_colors_from_url(image_url):
#     # Download the image from the URL
#     response = requests.get(image_url)
#     image_bytes = BytesIO(response.content)

#     # Instantiate ColorThief with the image bytes
#     color_thief = ColorThief(image_bytes)

#     # Get the dominant color
#     dominant_color = color_thief.get_color(quality=1)

#     # Get the palette of colors from the image
#     palette = color_thief.get_palette(color_count=2)

#     return dominant_color, palette

# # Example usage:
# image_url = "https://i.scdn.co/image/ab67616d0000b273e2d88ce9b368639664aa7847"
# dominant_color, palette = extract_main_colors_from_url(image_url)

# print("Dominant Color:", dominant_color)
# print("Palette:", palette)