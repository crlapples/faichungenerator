import os
from PIL import Image

# The folder with your processed, transparent character images.
TARGET_FOLDER = 'processed_web_characters'

def recenter_image(image_path):
    """
    Opens an image, finds the character, and saves a new version
    with the character perfectly centered.
    """
    try:
        with Image.open(image_path) as img:
            # Ensure the image is in RGBA format to handle transparency
            img = img.convert("RGBA")

            # Get the bounding box of the non-transparent parts of the image.
            # This returns (left, upper, right, lower) or None if the image is empty.
            bbox = img.getbbox()

            if bbox is None:
                print(f"Skipping empty image: {os.path.basename(image_path)}")
                return

            # Crop the image to the character's bounding box
            character_crop = img.crop(bbox)
            
            # Get the size of the original canvas and the cropped character
            canvas_width, canvas_height = img.size
            char_width, char_height = character_crop.size

            # Create a new, completely transparent image with the same dimensions
            new_img = Image.new("RGBA", (canvas_width, canvas_height), (0, 0, 0, 0))

            # Calculate the top-left coordinate to paste the character for perfect centering
            paste_x = (canvas_width - char_width) // 2
            paste_y = (canvas_height - char_height) // 2

            # Paste the cropped character onto the new transparent canvas
            new_img.paste(character_crop, (paste_x, paste_y))

            # Save the new, centered image, overwriting the old one
            new_img.save(image_path)
            
    except Exception as e:
        print(f"Could not process {os.path.basename(image_path)}: {e}")


# --- Main script execution ---
print(f"Starting auto-centering process for images in '{TARGET_FOLDER}'...")
print("Please ensure you have backed up this folder before proceeding.")

# Get a list of all files to process
try:
    all_files = [f for f in os.listdir(TARGET_FOLDER) if f.lower().endswith('.png')]
    total_files = len(all_files)
    print(f"Found {total_files} images to process.")
except FileNotFoundError:
    print(f"Error: The folder '{TARGET_FOLDER}' was not found. Please check the name.")
    exit()


# Loop through all the PNG files in the target folder
for i, filename in enumerate(all_files):
    # Print progress
    print(f"Processing [{i+1}/{total_files}]: {filename}")
    full_path = os.path.join(TARGET_FOLDER, filename)
    recenter_image(full_path)

print("\nAuto-centering process complete!")
