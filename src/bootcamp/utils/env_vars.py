import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME")
TEMPERATURE = os.getenv("TEMPERATURE")

INPUT_FILE_PATH = os.getenv("INPUT_FILE_PATH")

# Validate the environment variables

if not MODEL_NAME:
    raise ValueError("MODEL_NAME environment variable is required")

if not TEMPERATURE:
    raise ValueError("TEMPERATURE environment variable is required")

if not INPUT_FILE_PATH:
    raise ValueError("INPUT_FILE_PATH environment variable is required")

try:
    TEMPERATURE = float(TEMPERATURE)
except ValueError:
    raise ValueError("TEMPERATURE must be a float")
