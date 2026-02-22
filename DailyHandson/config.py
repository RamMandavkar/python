"""
Minimal configuration file for the Scam Detection project.
Contains only the essential settings used across the project.
"""

import sys
import os
import numpy as np
from pathlib import Path
from dotenv import load_dotenv

# Application Configuration
APP_NAME = "Scam Detection with LLMs"
REPEATABLE = 150

# Get project root directory
PROJECT_ROOT = Path(__file__).parent

# Paths
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
LOGS_DIR = PROJECT_ROOT / "logs"

# Create output directories if they don't exist
OUTPUTS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Load environment variables from .env file
#load_dotenv(PROJECT_ROOT / ".env")
load_dotenv() # loads .env into environment

# API Configuration
GEMINI_API_KEY = os.getenv("gemini_api_key")
GEMINI_MODEL_NAME=os.getenv("gemini_model_name")

# LLM Settings
DEFAULT_MODEL = "gemini-2.5-flash"
MAX_RETRIES = 3
RETRY_DELAY = 2

# Dataset Configuration
DEFAULT_DATASET = PROJECT_ROOT / "scam_detection_dataset.csv"
TEST_DATASET = PROJECT_ROOT / "test_scam_dataset.csv"

# Text column names to look for in datasets
TEXT_COLUMNS = ["text", "message_text", "message"]
LABEL_COLUMN = "label"


