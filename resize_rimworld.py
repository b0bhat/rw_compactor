from PIL import Image
import os
import logging
from concurrent.futures import ThreadPoolExecutor
from itertools import count

Image.MAX_IMAGE_PIXELS = None

# Define the maximum areas (in pixels) for different categories.
category_limits = {
    'Furniture':200,
    'Building': 380,
    'Pawn': 120,
    'Terrain': 1000,
    'category_Other': 300, 
    'category_Small': 100,
    'AerocraftFramework': 320,
    'Vehicles': 300,
    'Aircraft':320,
    'GenericProjections': 200,
    'ProjectionMasks25': 200,
    'ProjectionMasks50': 200,
    'ProjectionMasks75': 200,
    'GenericProjections': 200
}

category_skip = {
    'About',
    'Themes',
    'Heads',
    'Pollution',
    'ColonistBar',
}

category_small = {
    'Item',
    'Weapons',
    'Drugs',
    'Plant',
    'Headgear',
    'Projectile',
    'Plants',
    'Equipment',
    'Resource',
    'UI',
    'Accessories',
    'Artifacts',
}

resized, skipped, failed = 0,0,0
file_counter = count(start=1)

def process_file(input_path, folder_names):
    global resized, skipped, failed
    skip_this = any(name in category_skip for name in folder_names)
    limit = next((category_limits.get(name) for name in folder_names if name in category_limits), category_limits["category_Other"])
    if skip_this:
        skipped += 1
    else:
        try:
            with Image.open(input_path) as img:
                width, height = img.size
                if width > limit and height > limit:
                    aspect_ratio = width / height
                    new_size = (int(limit * aspect_ratio), limit) if width > height else (limit, int(limit / aspect_ratio))
                    img.resize(new_size, Image.Resampling.LANCZOS).save(input_path, 'PNG')
                    resized += 1
                else:
                    skipped += 1
        except Exception as e:
            logging.error(f"Failed: {input_path} - {e}")
            failed += 1
def main():
    global resized, skipped, failed
    base_dir = os.path.dirname(os.path.realpath(__file__))
    file_paths = [
        (os.path.join(root, file), root.split(os.path.sep)[::-1])
        for root, _, files in os.walk(base_dir) for file in files if file.endswith('.png')
    ]

    with ThreadPoolExecutor() as executor:
        executor.map(lambda args: process_file(*args), file_paths)

    logging.info(f"Done. Resized: {resized}, Skipped: {skipped}, Failed: {failed}")

if __name__ == "__main__":
    main()

