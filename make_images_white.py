import os
from PIL import Image

# This should be your folder of centered, transparent characters
SOURCE_FOLDER = 'processed_web_characters'

print(f"Starting to convert images in '{SOURCE_FOLDER}' to white...")

try:
    all_files = [f for f in os.listdir(SOURCE_FOLDER) if f.lower().endswith('.png')]
    total_files = len(all_files)
    print(f"Found {total_files} images to process.")
except FileNotFoundError:
    print(f"Error: The folder '{SOURCE_FOLDER}' was not found.")
    exit()

for i, filename in enumerate(all_files):
    full_path = os.path.join(SOURCE_FOLDER, filename)
    try:
        with Image.open(full_path) as img:
            img = img.convert("RGBA")
            pixels = img.load()

            for x in range(img.width):
                for y in range(img.height):
                    # If the pixel is not fully transparent, make it pure white
                    if pixels[x, y][3] > 0:
                        pixels[x, y] = (255, 255, 255, pixels[x, y][3]) # White + original alpha

            img.save(full_path)
            print(f"Processing [{i+1}/{total_files}]: Converted {filename} to white.")
    except Exception as e:
        print(f"Could not process {filename}: {e}")

print("\nImage conversion to white complete!")
