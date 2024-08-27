import os

from PIL import Image

from config.config_manager import ConfigMixin
from dual_universe.src.utils.read_json import read_json

script_dir = os.path.dirname(os.path.abspath(__file__))
json_dir = os.path.join(script_dir, "..", "json/config.json")
config_manager = ConfigMixin(json_dir)


assets_data = read_json(config_manager.get_value("config.assets_data"))

image_to_compare = "agg_hold"

image_file_path = assets_data.get("images", {}).get(f"{image_to_compare}.png")

# Open the PNG image
image = Image.open(image_file_path)

# Convert it to grayscale
grayscale_image = image.convert("L")

# Save the grayscale image
grayscale_image.save("../images/grayscale_image.png")
# Optionally, show the grayscale image
grayscale_image.show()
