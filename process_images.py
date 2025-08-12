import os
from PIL import Image

def process_character_image(input_path, output_path, character_color=(253, 224, 71)):
    """
    Processes a single character image: crops watermark, makes background
    transparent, and colorizes the character.

    Args:
        input_path (str): Path to the original black and white image.
        output_path (str): Path to save the processed transparent PNG.
        character_color (tuple): The new (R, G, B) color for the character.
    """
    try:
        with Image.open(input_path) as img:
            # Convert to Grayscale ('L') to simplify processing
            img = img.convert("L")

            # --- 1. Crop the watermark ---
            # IMPORTANT: Measure the watermark area and adjust these values.
            # These values assume the watermark is in the bottom-right corner.
            # The box is a (left, upper, right, lower)-tuple.
            width, height = img.size
            # Example: Crop off the bottom 15% and the right 15% of the image.
            crop_box = (0, height * 0.05, width, height * 0.95)
            img = img.crop(crop_box)
            # Resize back to original dimensions to maintain consistency
            img = img.resize((width, height), Image.Resampling.LANCZOS)

            # --- 2. Make background transparent and colorize character ---
            # Create a new, fully transparent image of the same size
            processed_img = Image.new("RGBA", img.size, (0, 0, 0, 0))

            # Get the pixel data to manipulate it
            pixels = img.load()
            processed_pixels = processed_img.load()

            for x in range(img.width):
                for y in range(img.height):
                    # Get the grayscale value of the pixel
                    grayscale_value = pixels[x, y]

                    # This threshold determines what is "black" (character) vs "white" (background)
                    # Adjust this value if your characters are faint or backgrounds are grayish.
                    if grayscale_value < 100:  # This pixel is part of the character
                        processed_pixels[x, y] = character_color + (255,) # Set to gold, fully opaque
                    # Otherwise, the pixel remains transparent from the initial state

            # Save the final processed image
            processed_img.save(output_path, "PNG")

    except FileNotFoundError:
        print(f"Error: Could not find the file {input_path}")
    except Exception as e:
        print(f"An error occurred while processing {input_path}: {e}")

# --- Batch Processing ---
# 1. Unzip your characters into a folder named 'original_characters'
# 2. Make sure this script is in the same directory as that folder.

original_folder = 'original_characters'
processed_folder = 'processed_web_characters'

# Create the output directory if it doesn't exist
os.makedirs(processed_folder, exist_ok=True)

print("Starting batch processing of character images...")

# Loop through all files in the original folder
for filename in os.listdir(original_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        # Assumes the filename is the character itself (e.g., '理.jpg')
        char_name = os.path.splitext(filename)[0]
        input_image_path = os.path.join(original_folder, filename)
        output_image_path = os.path.join(processed_folder, f"{char_name}.png") # PNG supports transparency

        print(f"Processing {filename} -> {char_name}.png")
        process_character_image(input_image_path, output_image_path, character_color=(253, 224, 71))

print(f"Batch processing complete! Images are saved in '{processed_folder}'.")
