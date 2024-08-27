import time
from concurrent.futures import ThreadPoolExecutor

import cv2
import cv2 as cv
import mss
import numpy as np
import pyautogui
from dual_universe.logs.logging_config import logger

from dual_universe.src.querysets import ImageQuerySet


class IdentifyScreen:
    def __init__(self):
        self.w, self.h = pyautogui.size()
        self.needle_images = self.load_needle_images_from_db()

    def load_needle_images_from_db(self):
        needle_images = {}
        images = ImageQuerySet.get_all_images()
        for image_data in images:
            image_path = image_data.image_url
            needle_img = cv.imread(image_path, cv.IMREAD_UNCHANGED)
            needle_images[image_data.image_name] = needle_img
        return needle_images

    def get_screenshot(self):
        with mss.mss() as sct:
            # Get information about the primary monitor
            monitor = {"top": 0, "left": 0, "width": self.w, "height": self.h}
            # Capture the screen
            img = sct.grab(monitor)
            # Convert the image to an array
            image_array = np.array(img)
            # Process the image
            found_filenames = self.process_image(image_array)
            filenames = []
            for filename in found_filenames:
                filename = ImageQuerySet.read_image_by_name(filename[0])
                filenames.append(filename.image_location)
            return filenames
            # Draw bounding boxes on the image
            # self.draw_bounding_boxes(image_array, found_filenames)

    def draw_bounding_boxes(self, image_array, found_filenames):
        if (
            found_filenames
        ):  # Display image with bounding boxes only if there are detected objects
            for filename, confidence in found_filenames:
                needle_img = self.needle_images[filename]
                h, w = needle_img.shape[:2]
                result = cv.matchTemplate(image_array, needle_img, cv.TM_CCOEFF_NORMED)
                _, _, _, max_loc = cv.minMaxLoc(result)
                top_left = max_loc
                bottom_right = (top_left[0] + w, top_left[1] + h)
                cv.rectangle(image_array, top_left, bottom_right, (0, 255, 0), 2)
                cv.putText(
                    image_array,
                    f"{filename} - {confidence:.2f}",
                    (top_left[0], top_left[1] - 10),
                    cv.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    1,
                )

            # Display the image with bounding boxes
            cv.imshow("Object Detection", image_array)
            cv.waitKey(1)

    def process_image(self, image_array):
        try:
            found_filenames = []  # Initialize list to store found filenames
            with ThreadPoolExecutor() as executor:
                futures = []
                for filename, needle_img in self.needle_images.items():

                    futures.append(
                        executor.submit(
                            self.match_template, image_array, needle_img, filename
                        )
                    )
                for future in futures:
                    result = future.result()
                    if result:
                        found_filenames.append(result)  # Collect the found filenames
            return found_filenames  # Return the found filenames
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            return []
        finally:
            return found_filenames

    def match_template(self, image_array, needle_img, filename):
        _needle_img = cv2.convertScaleAbs(needle_img)
        result = cv.matchTemplate(image_array, _needle_img, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        threshold = 0.80
        if max_val >= threshold:
            logger.info(
                f"Found needle: {filename} - {max_val} match | threshold: {threshold}"
            )
            # Return the filename and confidence level if a match is found
            return filename, max_val
        else:
            return None


def IdentifyScreen_main():
    start_time = time.perf_counter()
    _id_screen = IdentifyScreen()
    # _id_screen.get_screenshot()
    results = _id_screen.get_screenshot()
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time}")
    return results


if __name__ == "__main__":
    # cProfile.run("main()")
    IdentifyScreen_main()
