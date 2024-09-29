import json
import os
from pathlib import Path


def get_current_db(db_extension=".db"):
    root_directory = "../../.."
    """
    Search for a file with a specific extension in the root directory using pathlib.

    Args:
    root_directory (str): Path to the root directory.
    db_extension (str): Extension of the database file (default is ".db").

    Returns:
    str: The name of the database file found, or None if not found.
    """
    # Create a Path object for the root directory
    root_path = Path(root_directory)

    # Search for files in the root directory with the given extension
    for file_path in root_path.iterdir():
        if file_path.is_file() and file_path.suffix == db_extension:
            print(f"Database found: {file_path.name}")
            return file_path.name

    raise ValueError("No database file found in the root directory.")


def get_user_choice(options, prompt):
    """
    Display a list of options and prompt the user to choose one by number.

    Args:
    options (list): A list of options to choose from.
    prompt (str): The prompt message for the user.

    Returns:
    str: The selected option.
    """
    print(prompt)
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")

    while True:
        try:
            choice = int(input("Enter the number corresponding to your choice: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print(
                    f"Invalid choice. Please select a number between 1 and {len(options)}."
                )
        except ValueError:
            print("Invalid input. Please enter a number.")


def update_config_file(file_path):
    # Load the existing JSON structure (optional: if you want to load from an existing file)
    config_data = {
        "config": {
            "pilot": "",
            "game_client": "",
            "active_mission_name": "",
            "active_characters": "",
            "database": "",
        }
    }

    # Pre-defined options for game_client, active_mission_name, and active_characters
    game_client_options = ["GeForceNOW", "Steam", "Desktop Client", "MyDU"]
    mission_name_options = [
        "Pure Sulfur Shipment",
        "Iron Ore Delivery",
        "Gold Expedition",
    ]

    # Function to ensure that a required value is not left blank
    def get_required_input(prompt):
        while True:
            value = input(prompt)
            if value.strip():
                return value
            else:
                print("This field cannot be blank. Please enter a value.")

    # Request user input for each key
    config_data["config"]["database"] = get_current_db()

    config_data["config"]["pilot"] = get_required_input(
        "Enter pilot name (required): "
    ).lower()

    config_data["config"]["game_client"] = get_user_choice(
        game_client_options, "Choose a game client:"
    ).lower()

    config_data["config"]["active_mission_name"] = get_user_choice(
        mission_name_options, "Choose an active mission:"
    ).lower()

    user_list_input = input("Enter user list (default: user): ")
    config_data["config"]["active_characters"] = (
        user_list_input if user_list_input else "user"
    )

    # Write the updated data back to the file
    with open(file_path, "w") as f:
        json.dump(config_data, f, indent=4)

    print(f"Configuration updated and saved to {file_path}")


if __name__ == "__main__":
    # Call the function to update the config file
    file_path = "../../../config.json"
    update_config_file(file_path)
