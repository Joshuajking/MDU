import csv
import json
import os

import numpy as np
from dual_universe.logs.logging_config import logger

from config import config_manager
from dual_universe.path_router import DirectoryPaths
from dual_universe.settings import IMAGES_DIR, ASSETS_DATA
from dual_universe.util.read_json import read_json


def conf_startup():
    game = input("What game are you playing?")

    # Prompt the user for input
    pilot_name = input("Enter Pilot name: ").capitalize()

    try:
        # List existing JSON files in the user_list directory
        user_list_directory = os.path.join(JSON_DIR)
    except FileNotFoundError:
        logger.error(f"file not found: {user_list_directory}")

    try:
        json_files = [
            file
            for file in os.listdir(os.path.dirname(user_list_directory))
            if file.endswith(".json") and file.startswith("user")
        ]
    except FileNotFoundError as e:
        logger.error(f"file not found: {user_list_directory}: {str(e)}")
    # Store the list of JSON files and their character data where the pilot's name is found
    json_files_with_pilot = []

    # Loop through each JSON file and collect character data where the pilot's name is found
    for json_file in json_files:
        try:
            stripped_dir = os.path.dirname(user_list_directory)
            json_path = os.path.join(stripped_dir, json_file)
            with open(json_path, "r") as file:
                json_data = json.load(file)
        except Exception as e:
            logger.error(f"{str(e)}")
        if pilot_name in json_data.get("characters", {}):
            json_files_with_pilot.append(
                (json_path, json_data["characters"][pilot_name])
            )

    # Display the list of JSON files where the pilot's name is found
    if json_files_with_pilot:
        print(f"Pilot name '{pilot_name}' found in the following JSON files:")
        for index, (json_path, _) in enumerate(json_files_with_pilot, start=1):
            print(f"{index}. {json_path}")
    else:
        print(f"Pilot name '{pilot_name}' not found in any JSON files.")
        exit(1)

    # Prompt the user to choose a JSON file
    chosen_index = (
        int(input("Choose a JSON file (enter the corresponding number): ")) - 1
    )

    if chosen_index < 0 or chosen_index >= len(json_files_with_pilot):
        print("Invalid choice.")
        exit(1)

    chosen_json_path, pilot_character_data = json_files_with_pilot[chosen_index]

    # Give the user a choice for the game_client
    print("Choose a game_client:")
    print("1. Dual universe")
    print("2. Dual universe on GeForce Now")
    client_choice = input("Enter the corresponding number: ")

    if client_choice == "1":
        game_client = "Dual Universe"
    elif client_choice == "2":
        game_client = "Dual Universe on GeForce Now"
    else:
        print("Invalid choice.")
        exit(1)

    # Generate configuration file content
    # TODO: have user input for client_app_path
    config_file_content = f"""
	[pilot_character]
	PILOT = {pilot_name}
	
	[character_list]
	JSON_FILE = {chosen_json_path}
	
	[window_title]
	WINDOW_TITLE = {"Dual.exe"}
	
	[game_client]
	CLIENT = "{game_client}"
	
	[client_app_path]    
	CLIENT_APP_PATH = r"C:\ProgramData\Dual Universe\Game\DualUniverse.exe"
	
	[log_size]
	MAX_SIZE = {1024}
	"""

    # Save configuration file
    output_file = "../src/config/config.conf"
    try:
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, "w") as file:
            file.write(config_file_content)
    except FileNotFoundError:
        print(f'Could not write config file "{output_file}"')
    except IOError as e:
        print(f'Error writing config file "{output_file}": {e}')
    logger.info(f"Configuration file '{output_file}' generated.")


def create_character_json(input_file, output_file):
    nested_dict = {"characters": {}}

    with open(input_file, "r", newline="", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            username = row["username"]
            character_info = {
                "email": row["email"],
                "pwd": row["password"],
            }
            nested_dict["characters"][username] = character_info

    with open(output_file, "w") as file:
        json.dump(nested_dict, file, indent=2)


def ocr_engine():
    from time import sleep
    import pyautogui
    import pytesseract
    import json

    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )

    # Define the coordinates of the row to capture screenshots from
    row_coordinates = {
        "top_left_x": 863,
        "top_left_y": 275,
        "bottom_right_x": 1728,
        "bottom_right_y": 505,
    }

    # Define the custom headers
    custom_headers = [
        "Title",
        "Issued_by",
        "Safe_zone",
        "Distance",
        "Ride",
        "Mass",
        "Volume",
        "Time_remaining",
        "Coll",
        "Reward",
    ]

    cell_coordinates = {
        "Title": {
            "top_left_x": 890,
            "top_left_y": 275,
            "bottom_right_x": 1040,
            "bottom_right_y": 310,
        },
        "Issued_by": {
            "top_left_x": 1040,
            "top_left_y": 275,
            "bottom_right_x": 1125,
            "bottom_right_y": 310,
        },
        "Safe_zone": {
            "top_left_x": 1125,
            "top_left_y": 275,
            "bottom_right_x": 1180,
            "bottom_right_y": 310,
        },
        "Distance": {
            "top_left_x": 1180,
            "top_left_y": 275,
            "bottom_right_x": 1270,
            "bottom_right_y": 310,
        },
        "Ride": {
            "top_left_x": 1270,
            "top_left_y": 275,
            "bottom_right_x": 1340,
            "bottom_right_y": 310,
        },
        "Mass": {
            "top_left_x": 1330,
            "top_left_y": 275,
            "bottom_right_x": 1395,
            "bottom_right_y": 310,
        },
        "Volume": {
            "top_left_x": 1400,
            "top_left_y": 275,
            "bottom_right_x": 1470,
            "bottom_right_y": 310,
        },
        "Time_remaining": {
            "top_left_x": 1470,
            "top_left_y": 275,
            "bottom_right_x": 1570,
            "bottom_right_y": 310,
        },
        "Coll": {
            "top_left_x": 1570,
            "top_left_y": 275,
            "bottom_right_x": 1625,
            "bottom_right_y": 310,
        },
        "Reward": {
            "top_left_x": 1625,
            "top_left_y": 275,
            "bottom_right_x": 1680,
            "bottom_right_y": 310,
        },
    }

    data = []

    # Scroll and repeat until no new data
    prev_data_length = 0
    scroll_step = -80
    sleep(5)
    while True:
        new_data = []

        # Capture screenshots of each cell in the row
        for header in custom_headers:
            coords = cell_coordinates[header]
            cell_screenshot = pyautogui.screenshot(
                region=(
                    coords["top_left_x"],
                    coords["top_left_y"],
                    coords["bottom_right_x"] - coords["top_left_x"],
                    coords["bottom_right_y"] - coords["top_left_y"],
                )
            )
            cell_text = pytesseract.image_to_string(cell_screenshot).strip()
            new_data.append({header: cell_text})

        # Check if new data was extracted
        # Scroll down
        pyautogui.moveTo(1723, 290)
        pyautogui.scroll(scroll_step, 1723, 290)
        sleep(0.5)
        if len(new_data) == prev_data_length:
            break  # No new data, exit loop

        # Update the previous data length
        prev_data_length = len(new_data)

        # Scroll down
        pyautogui.scroll(scroll_step, 1723, 290)

        # Sleep for a moment to allow for the screen to adjust
        sleep(1)

        # Append new data to the main data list
        data.extend(new_data)

    # Create JSON file
    json_filename = "processed_row_data.json"
    with open(json_filename, "w") as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Processed row data saved to {json_filename}")


def generate_assets_data():
    __assets_data_json = ASSETS_DATA

    def get_folder_and_file_info(folder_path):
        folder_info = {}
        for root, dirs, files in os.walk(folder_path):
            folder_name = os.path.basename(root)
            file_info = {file: os.path.join(root, file) for file in files}
            folder_info[folder_name] = file_info
        return folder_info

    folder_file_info = get_folder_and_file_info(IMAGES_DIR)

    output_json_path = __assets_data_json
    with open(output_json_path, "w") as json_file:
        json.dump(folder_file_info, json_file, indent=4)

    print("JSON file created successfully.")


def collect_change_json_format(**kwargs):
    # __transformed_data_file = os.path.join(json_dir, "transformed_data.json")
    __assets_data_json = ASSETS_DATA
    image_to_compare = kwargs.get("image_to_compare")
    screen_coords = kwargs.get("screen_coords")
    bbox = kwargs.get("bbox")
    # Your code to get the image details

    # Create a tuple to represent your data
    image_data = f"{IMAGES_DIR}/{image_to_compare}.png"

    # Define the path to the .txt file
    txt_file_path = "image_data.txt"

    # Append the image data to the .txt file
    with open(txt_file_path, "a") as txt_file:
        txt_file.write(str(image_data) + "\n")

    print(f"Appended data for '{image_to_compare}.png' to {txt_file_path}.")


def change_json_format(**kwargs):
    image_to_compare = kwargs.get("image_to_compare")
    screen_coords = kwargs.get("screen_coords")
    bbox = kwargs.get("bbox")
    # Find the ImageData record with the specified image name
    query = ImageData.update(
        x_coordinate=coordinates[0],
        y_coordinate=coordinates[1],
        width=coordinates[2],
        height=coordinates[3],
    ).where(ImageData.img_name == image_name)

    # Execute the update query
    updated_rows = query.execute()

    left, top, width, height = bbox
    entry = {
        "path": f"{IMAGES_DIR}/{image_to_compare}.png",
        "bbox": [left, top, width, height],
    }
    # Create a tuple to represent your data
    image_data = (f"{IMAGES_DIR}/{image_to_compare}.png", [left, top, width, height])

    # Convert any int64 values to regular Python integers
    def convert_int64_to_int(obj):
        if isinstance(obj, np.int64):
            return int(obj)
        return obj

    try:
        # Read existing data from the .txt file
        existing_data = []
        try:
            with open(__transformed_data_file, "r") as txt_file:
                existing_data = txt_file.readlines()
        except FileNotFoundError:
            pass

        # Create a tuple to represent your data
        image_data = (
            f"{IMAGES_DIR}/{image_to_compare}.png",
            [left, top, width, height],
        )

        # Append the image data to the .txt file
        with open(__transformed_data_file, "w") as txt_file:
            # Append the new data
            existing_data.append(str(image_data) + "\n")
            txt_file.writelines(existing_data)

    except Exception as e:
        print(str(e))
        logger.exception(f"Exception: {e}", exc_info=True)

    print(f"Appended data for '{image_to_compare}.png' to {__transformed_data_file}.")


def get_folder_and_file_info(folder_path):
    """Walks the folder"""
    folder_info = {}
    for root, dirs, files in os.walk(folder_path):
        folder_name = os.path.basename(root)
        file_info = {file: os.path.join(root, file) for file in files}
        folder_info[folder_name] = file_info
    return folder_info


def assets_json_structure():
    """Creates path for altered or added image files during start up"""
    folder_file_info = get_folder_and_file_info(DirectoryPaths.IMAGES_DIR)

    last_modification_time = max(
        os.path.getmtime(file_path)
        for folder_info in folder_file_info.values()
        for file_path in folder_info.values()
    )
    output_json_path = os.path.join(DirectoryPaths.JSON_DIR, "assets_data.json")
    if os.path.exists(output_json_path):
        json_modification_time = os.path.getmtime(output_json_path)
        if last_modification_time <= json_modification_time:
            logger.info("No modifications in data directory. Skipping JSON update.")
            return
    try:
        with open(output_json_path, "w") as json_file:
            json.dump(folder_file_info, json_file, indent=4)
    except FileNotFoundError as e:
        logger.warning(f"File not found at {output_json_path}: {str(e)}")
    print("JSON file created or updated successfully.")
    logger.info("JSON file created or updated successfully.")


def modify_assets_json_path():
    """
    Modify assets_data.json file paths according to the new directory structure that images resides in
    :return: new value, in key: value dict
    """
    # Load the JSON data from the file
    assets_data_path = os.path.join(DirectoryPaths.JSON_DIR, "assets_data.json")
    # Path to images directory
    images_path = os.path.join(DirectoryPaths.IMAGES_DIR)
    # Load the JSON data from the file
    with open(assets_data_path, "r") as f:
        data = json.load(f)

    # Define the new directory path
    new_dir_value = images_path  # Update with the new directory path

    # Iterate over each key-value pair in the "images" dictionary
    for key, value in data["images"].items():
        # remove file name of the value path
        old_dir_value = os.path.dirname(value)
        # Replace the directory part of the value with the new directory path
        data["images"][key] = value.replace(
            old_dir_value,
            new_dir_value,
            # r'C:\Repositories\Dual Universe\Missions Dual Universe\util\..\images', new_dir
        )

    # Save the updated JSON data back to the file
    with open(assets_data_path, "w") as f:
        json.dump(data, f, indent=4)


def convert_json_to_txt():
    try:
        # Assuming ASSETS_DATA is a string containing JSON data
        json_file = read_json(config_manager.get_value("config.assets_data"))

        # Print the content of ASSETS_DATA for debugging
        print("ASSETS_DATA content:", json_file)

        with open("../dual_universe/data/json/assets_data.txt", "w") as txt_file:
            for var, path in json_file.items():
                txt_file.writelines(f"{var}: {path}\n")

        print("Conversion complete. Check '../json/assets_data.txt' for the result.")
    except json.JSONDecodeError as json_error:
        print(f"JSON decoding error: {json_error}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# def get_image_bbox(image_path, region_name, grayscale=False):
# 	screen_coords = pyautogui.locateOnScreen(image_path, minSearchTime=3, confidence=0.9, grayscale=grayscale)
# 	if screen_coords is not None:
# 		left, top, width, height = screen_coords
# 		right = left + width
# 		bottom = top + height
# 		center_x = left + width // 2
# 		center_y = top + height // 2
# 		pyautogui.moveTo(center_x, center_y)
# 		SearchAreaQuerySet.create_or_update_search_area(region_name, {
# 			"left": int(left),
# 			"top": int(top),
# 			"right": int(right),
# 			"bottom": int(bottom),
# 			"center_x": int(center_x),
# 			"center_y": int(center_y)
# 		})
# 		return
# 	raise ValueError(f"region_name: {region_name} was not found in")


def see_image():
    # Directory path containing the directories (screens) with images
    screens_directory = r"C:\Users\joshu\Pictures\DU mission thumbnails"

    # Output JSON file path
    output_json_file = r"C:\Repositories\Dual Universe\Missions Dual Universe\data\json\transformed_data.json"

    # Dictionary to store found images
    found_images = {}

    # Loop through all directories (screens)
    for screen_name in os.listdir(screens_directory):
        screen_path = os.path.join(screens_directory, screen_name)
        if os.path.isdir(screen_path):
            # Loop through all files (images) in the directory
            for filename in os.listdir(screen_path):
                if filename.endswith(".png"):
                    # Process the image file
                    image_path = os.path.join(screen_path, filename)
                    print(f"Processing image: {image_path}")
                    bbox = get_image_bbox(image_path)
                    if bbox:
                        left, top, right, bottom, center_x, center_y = bbox
                        # Add image information to the dictionary
                        image_info = {
                            "image_name": filename,
                            "image_location": screen_name,
                            "image_url": image_path,
                            "image_bbox": {
                                "left": left,
                                "top": top,
                                "right": right,
                                "bottom": bottom,
                                "center_x": center_x,
                                "center_y": center_y,
                            },
                        }
                        found_images[filename] = image_info

    # Write the found images dictionary to a JSON file
    with open(output_json_file, "w") as json_file:
        json.dump(found_images, json_file, indent=4)

    print("Found images information saved to:", output_json_file)


if __name__ == "__main__":
    from models.models import SearchAreaLocation

    origin_dict = {
        "ACTIVE_TAKEN_MISSIONS": {
            "region_name": SearchAreaLocation.ACTIVE_TAKEN_MISSIONS,
            "image_path": r"C:\Repositories\Dual Universe\Missions Dual Universe\data\search_areas\ACTIVE_TAKEN_MISSIONS.png",
        },
        "AVAILABLE_MISSIONS": {
            "region_name": SearchAreaLocation.AVAILABLE_MISSIONS,
            "image_path": r"C:\Repositories\Dual Universe\Missions Dual Universe\data\search_areas\AVAILABLE_MISSIONS.png",
        },
        "RETRIEVE_DELIVERY_STATUS": {
            "region_name": SearchAreaLocation.RETRIEVE_DELIVERY_STATUS,
            "image_path": r"C:\Repositories\Dual Universe\Missions Dual Universe\data\search_areas\unselected_deliver_package.png",
        },
    }

    region_dict = {
        "ACTIVE_TAKEN_MISSIONS": {
            "region_name": SearchAreaLocation.ACTIVE_TAKEN_MISSIONS,
            "image_path": r"C:\Repositories\Dual Universe\Missions Dual Universe\data\search_areas\ACTIVE_TAKEN_MISSIONS.png",
        },
        "AVAILABLE_MISSIONS": {
            "region_name": SearchAreaLocation.AVAILABLE_MISSIONS,
            "image_path": r"C:\Repositories\Dual Universe\Missions Dual Universe\data\search_areas\AVAILABLE_MISSIONS.png",
        },
        "RETRIEVE_DELIVERY_STATUS": {
            "region_name": SearchAreaLocation.RETRIEVE_DELIVERY_STATUS,
            "image_path": r"C:\Repositories\Dual Universe\Missions Dual Universe\data\search_areas\unselected_deliver_package.png",
        },
        "DEST_INFO": {
            "region_name": SearchAreaLocation.DEST_INFO,
            "image_path": r"C:\Repositories\Dual Universe\Missions Dual Universe\data\search_areas\DEST_INFO.png",
        },
        "MISSION_META": {
            "region_name": SearchAreaLocation.MISSION_META,
            "image_path": r"C:\Repositories\Dual Universe\Missions Dual Universe\data\search_areas\MISSION_META.png",
        },
        "ORIGIN_INFO": {
            "region_name": SearchAreaLocation.ORIGIN_INFO,
            "image_path": r"C:\Repositories\Dual Universe\Missions Dual Universe\data\search_areas\ORIGIN_INFO.png",
        },
        "PACKAGE_INFO": {
            "region_name": SearchAreaLocation.PACKAGE_INFO,
            "image_path": r"C:\Repositories\Dual Universe\Missions Dual Universe\data\search_areas\PACKAGE_INFO.png",
        },
        "REWARD_INFO": {
            "region_name": SearchAreaLocation.REWARD_INFO,
            "image_path": r"C:\Repositories\Dual Universe\Missions Dual Universe\data\search_areas\REWARD_INFO.png",
        },
        "TITLE_INFO": {
            "region_name": SearchAreaLocation.TITLE_INFO,
            "image_path": r"C:\Repositories\Dual Universe\Missions Dual Universe\data\search_areas\TITLE_INFO.png",
        },
    }

    for key, value in region_dict.items():
        region_name = value["region_name"]
        image_path = value["image_path"]

        get_image_bbox(
            region_name=region_name,
            image_path=image_path,
            grayscale=True,
        )
