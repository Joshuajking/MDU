import os

import cv2 as cv
import pyautogui
from PIL import ImageGrab, Image

from config.config_manager import ConfigManager
from querysets.querysets import ImageQuerySet
from utils.read_json import read_json

script_dir = os.path.dirname(os.path.abspath(__file__))
config_json = os.path.join(script_dir, "..", "json/config.json")
images_dir = os.path.join(script_dir, "..", "du_images")

config_manager = ConfigManager()
assets_data = read_json(config_manager.get_value("config.assets_data"))


def convert_to_32_bit():
    # Set the path to your directory containing PNG files
    directory = r"../temp/ocr_enhanced_images"

    # Loop through all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            # Construct the full file path
            file_path = os.path.join(directory, filename)

            # Open the 24-bit PNG image
            image = Image.open(file_path)
            # Convert it to 32-bit by adding an alpha channel (transparency)
            if image.mode != "RGBA":
                image = image.convert("RGBA")

                # Save the 32-bit PNG image
                image.save(file_path)
            image.close()


def template_matching(image_to_compare):
    screen_w, screen_h = pyautogui.size()
    cell_screenshot = ImageGrab.grab(bbox=(0, 0, screen_w, screen_h))
    # Convert the screenshot to a 32-bit image
    cell_screenshot = cell_screenshot.convert("RGBA")
    screenshot = r"../temp/template_match_screenshot.png"
    cell_screenshot.save(screenshot)
    image1 = screenshot
    image_data = ImageQuerySet().read_image_by_name(image_name=image_to_compare)

    # Set the path to your directory containing PNG files
    haystack_img = cv.imread(image1, cv.IMREAD_UNCHANGED)

    needle_img = cv.imread(image_data.image_url, cv.IMREAD_UNCHANGED)

    result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)

    # get the best match position
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    # print("Best match top left position: %s" % str(max_loc))
    # print("Best match confidence: %s" % max_val)

    threshold = 0.80
    if max_val >= threshold:
        print(
            f"Found needle: {image_data.image_name} - {max_val} match | threshold: {threshold}"
        )
        # get dimensions of the needle image
        needle_w = needle_img.shape[1]
        needle_h = needle_img.shape[0]

        top_left = max_loc
        bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)

        cv.rectangle(
            haystack_img,
            top_left,
            bottom_right,
            color=(0, 255, 0),
            thickness=2,
            lineType=cv.LINE_4,
        )
        cv.imshow(f"{image_data.image_name}", haystack_img)
        cv.waitKey()

    else:
        print(
            f"Needle not found: {image_data.image_name} - {max_val} match | threshold: {threshold}"
        )


if __name__ == "__main__":
    template_matching(image_to_compare="password_login")
