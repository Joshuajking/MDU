import os

from loguru import logger

from router import DirectoryPaths

# Get the current working directory
# cwd = os.getcwd()

# Define the relative path to the logs directory
# log_dir = os.path.join(DirectoryPaths.ROOT_DIR, '')

# Ensure the log directory exists
# os.makedirs(log_dir, exist_ok=True)

# Configure the logger to write to a file and console
logger.add(
    os.path.join(DirectoryPaths.ROOT_DIR, "logfile.log"),
    rotation="500 MB",
    backtrace=True,
    diagnose=True,
)
