import os

from loguru import logger

# Get the current working directory
cwd = os.getcwd()

# Define the relative path to the logs directory
log_dir = os.path.join(cwd, "../logs")

# Ensure the log directory exists
os.makedirs(log_dir, exist_ok=True)

# Configure the logger to write to a file and console
logger.add(
    os.path.join(log_dir, "logfile.log"),
    rotation="500 MB",
    backtrace=True,
    diagnose=True,
)
