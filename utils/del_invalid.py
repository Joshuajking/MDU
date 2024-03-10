import os
import time


# script_dir = os.path.dirname(os.path.abspath(__file__))
# temp_dir = os.path.join(script_dir, '..', 'temp')
# invalid_images = os.path.join(script_dir, '..', 'templates/invalid_images')
# templates = os.path.join(script_dir, '..', 'templates')
# ocr_enhanced_images = os.path.join(script_dir, '...', 'temp/ocr_enhanced_images')
# # Define the directory where the images are located
# image_dirs = [temp_dir, templates]

# Define the maximum directory size in bytes (e.g., 100 MB)
max_dir_size = 0.5 * 1024 * 1024 * 1024   # 512 MB


def get_directory_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size


def delete_png_files_to_limit(directories, limit):
    for _directory in directories:
        while get_directory_size(_directory) > limit:
            png_files = [f for f in os.listdir(_directory) if f.lower().startswith('temp') and f.lower().endswith('.png')]
            if not png_files:
                break  # No more PNG files to delete

            png_files.sort(key=lambda x: os.path.getctime(os.path.join(_directory, x)))
            file_to_remove = os.path.join(_directory, png_files[0])
            os.remove(file_to_remove)
            print(f"Deleted {file_to_remove}")


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    temp_dir = os.path.join(script_dir, '..', 'temp')
    invalid_images = os.path.join(script_dir, '..', 'templates/invalid_images')
    templates = os.path.join(script_dir, '..', 'templates')
    ocr_enhanced_images = os.path.join(script_dir, '..', 'temp/ocr_enhanced_images')
    # Define the directory where the images are located
    image_dirs = [temp_dir, templates]
    while True:
        for directory in image_dirs:
            current_dir_size = get_directory_size(directory)
            print(f"Current directory size for {directory}: {current_dir_size} bytes")
            if current_dir_size > max_dir_size:
                delete_png_files_to_limit([directory], max_dir_size)
        time.sleep(1800)  # Check and delete files every half hour (adjust as needed)
