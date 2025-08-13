import os
import json
import re

processed_folder = 'processed_web_characters'
mapping = {}

print("Generating character-to-filename map...")

for filename in os.listdir(processed_folder):
    match = re.search(r'([\u4e00-\u9fa5])\.', filename)
    if match:
        # The character is the 'key'
        character = match.group(1)
        # The full filename is the 'value'
        mapping[character] = filename

# Write the map to a JSON file
with open('character_map.json', 'w', encoding='utf-8') as f:
    json.dump(mapping, f, ensure_ascii=False, indent=2)

print("'character_map.json' created successfully!")
