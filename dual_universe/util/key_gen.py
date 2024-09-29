from cryptography.fernet import Fernet
import os


def generate_and_store_key(key_file_path):
    # Generate a new Fernet key
    key = Fernet.generate_key()

    # Store the key in a file securely
    with open(key_file_path, "wb") as key_file:
        key_file.write(key)

    print(f"Fernet key generated and stored at: {key_file_path}")
    return key


def load_key(key_file_path):
    # Load the existing key from the key file
    if not os.path.exists(key_file_path):
        raise FileNotFoundError(
            "Key file not found. Please run the setup or regenerate the key."
        )

    with open(key_file_path, "rb") as key_file:
        key = key_file.read()

    return key


def get_key_path():
    # Get the user's home directory to store the key securely
    home_dir = os.path.expanduser("~")
    key_file_path = os.path.join(home_dir, ".mdu_key")
    return key_file_path


def setup_key():
    key_file_path = get_key_path()

    # Check if the key already exists
    if not os.path.exists(key_file_path):
        # Generate and store the key if it doesn't exist
        key = generate_and_store_key(key_file_path)
    else:
        # Load the existing key if found
        key = load_key(key_file_path)

    return key
