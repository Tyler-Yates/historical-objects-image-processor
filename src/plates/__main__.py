import os
import shutil

# This import is needed even though it is not called directly
# noinspection PyUnresolvedReferences
import pillow_avif
from PIL import Image

from src.util.constants import ROOT_PATH
from src.util.image_adjustments import resize_to_max_dimension


INPUT_DIRECTORY = os.path.join(ROOT_PATH, "input", "plates")
OUTPUT_DIRECTORY = os.path.join(ROOT_PATH, "output", "plates")
COMPLETED_DIRECTORY = os.path.join(ROOT_PATH, "completed", "plates")
HIGH_QUALITY = 50
LOW_QUALITY = 50
HI_MAX_DIMENSION = 2500
LOW_MAX_DIMENSION = 400


def process_plate_image(input_path: str):
    if not input_path.lower().endswith(".jpg"):
        print(f"ERROR: {input_path} is not a jpg file. Cannot process.")
        return

    plate_name = os.path.basename(input_path).split(".")[0]
    output_path = os.path.join(OUTPUT_DIRECTORY, plate_name)
    os.makedirs(output_path, exist_ok=True)

    input_image = Image.open(input_path)

    # Save the high quality image with no resizing
    hi_image = resize_to_max_dimension(input_image, HI_MAX_DIMENSION)
    hi_image.save(os.path.join(output_path, f"{plate_name}-hi.avif"), "AVIF", quality=HIGH_QUALITY)

    # Resize the image for the low quality gallery
    low_image = resize_to_max_dimension(input_image, LOW_MAX_DIMENSION)
    low_image.save(os.path.join(output_path, f"{plate_name}.avif"), "AVIF", quality=LOW_QUALITY)

    print(f"Finished processing {input_path}")


def main():
    os.makedirs(COMPLETED_DIRECTORY, exist_ok=True)

    for item in os.listdir(INPUT_DIRECTORY):
        item_path = os.path.join(INPUT_DIRECTORY, item)
        if os.path.isfile(item_path):
            process_plate_image(item_path)
            shutil.move(item_path, COMPLETED_DIRECTORY)
        else:
            print(f"ERROR!!!!!!! Ignoring item {item_path}")


if __name__ == '__main__':
    main()
