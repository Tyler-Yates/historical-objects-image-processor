import os
import shutil

# This import is needed even though it is not called directly
# noinspection PyUnresolvedReferences
import pillow_avif
from PIL import Image

from src.util.constants import ROOT_PATH
from src.util.image_adjustments import resize_to_max_dimension


INPUT_DIRECTORY = os.path.join(ROOT_PATH, "input", "medals")
OUTPUT_DIRECTORY = os.path.join(ROOT_PATH, "output", "medals")
COMPLETED_DIRECTORY = os.path.join(ROOT_PATH, "completed", "medals")
HIGH_QUALITY = 50
LOW_QUALITY = 50
HI_MAX_DIMENSION = 1500
LOW_MAX_DIMENSION = 400


def process_medal_image(input_path: str):
    if not input_path.lower().endswith(".jpg"):
        print(f"ERROR: {input_path} is not a jpg file. Cannot process.")
        return

    file_name = os.path.basename(input_path).split(".")[0]
    hi_gallery = os.path.join(OUTPUT_DIRECTORY, "hi")
    os.makedirs(hi_gallery, exist_ok=True)
    low_gallery = os.path.join(OUTPUT_DIRECTORY, "low")
    os.makedirs(low_gallery, exist_ok=True)

    input_image = Image.open(input_path)

    # Save the high quality image with no resizing
    hi_image = resize_to_max_dimension(input_image, HI_MAX_DIMENSION)
    hi_image.save(os.path.join(hi_gallery, f"{file_name}.avif"), "AVIF", quality=HIGH_QUALITY)

    # Resize the image for the low quality gallery
    low_image = resize_to_max_dimension(input_image, LOW_MAX_DIMENSION)
    low_image.save(os.path.join(low_gallery, f"{file_name}.avif"), "AVIF", quality=LOW_QUALITY)

    shutil.move(input_path, os.path.join(COMPLETED_DIRECTORY, os.path.basename(input_path)))

    print(f"Finished processing {input_path}")


def main():
    os.makedirs(COMPLETED_DIRECTORY, exist_ok=True)

    for item in os.listdir(INPUT_DIRECTORY):
        item_path = os.path.join(INPUT_DIRECTORY, item)
        if os.path.isfile(item_path):
            process_medal_image(item_path)
        else:
            print(f"Ignoring item {item_path}")


if __name__ == '__main__':
    main()
