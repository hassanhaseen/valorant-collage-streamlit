import os
import math
from PIL import Image
import zipfile

TIER_ORDER = ["exclusive", "ultra", "premium", "deluxe", "select", "unknown"]
COLLAGE_GRIDS = {2: 4, 3: 9, 4: 16, 5: 25, 6: 36, 7: 49, 8: 65, 9: 81}

def extract_tier(filename):
    prefix = filename.split('_')[0].lower()
    return TIER_ORDER.index(prefix) if prefix in TIER_ORDER else len(TIER_ORDER)

def sort_images_by_tier(paths):
    def get_tier_rank(path):
        filename = os.path.basename(path).lower()
        prefix = filename.split('_')[0]
        return TIER_ORDER.index(prefix) if prefix in TIER_ORDER else len(TIER_ORDER)

    return sorted(paths, key=get_tier_rank)


def choose_optimal_grid(total_images):
    for grid_size in sorted(COLLAGE_GRIDS.keys()):
        per_collage = COLLAGE_GRIDS[grid_size]
        if math.ceil(total_images / per_collage) <= 5:
            return grid_size, per_collage, math.ceil(total_images / per_collage)
    largest = max(COLLAGE_GRIDS.keys())
    return largest, COLLAGE_GRIDS[largest], 5

def chunk_fixed(images, per_collage, total_collages):
    chunks = []
    idx = 0
    for _ in range(total_collages):
        chunk = images[idx:idx + per_collage]
        chunks.append(chunk)
        idx += per_collage
    return chunks

def make_collage(image_paths, grid_size):
    cols = rows = grid_size
    thumb_w = 1200 // cols
    thumb_h = 1200 // rows
    collage = Image.new('RGB', (1200, 1200), 'black')

    for idx, path in enumerate(image_paths):
        try:
            img = Image.open(path).resize((thumb_w, thumb_h))
            x = (idx % cols) * thumb_w
            y = (idx // cols) * thumb_h
            collage.paste(img, (x, y))
        except:
            continue
    return collage

def generate_collages(images):
    grid_size, per_collage, num_collages = choose_optimal_grid(len(images))
    chunks = chunk_fixed(images, per_collage, num_collages)
    while len(chunks) < 5:
        chunks.append([])

    output_paths = []
    for i in range(5):
        collage = make_collage(chunks[i], grid_size)
        path = f"outputs/collage_{i+1}.jpg"
        collage.save(path)
        output_paths.append(path)
    return output_paths

def zip_collages(filepaths):
    zip_path = "outputs/collages.zip"
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for f in filepaths:
            zipf.write(f, os.path.basename(f))
    return zip_path
