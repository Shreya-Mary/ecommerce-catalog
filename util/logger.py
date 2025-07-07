# util/logger.py
import logging
import os

# Create logs directory if not exists
if not os.path.exists('logs'):
    os.makedirs('logs')

# Set up logger
logger = logging.getLogger("CatalogLogger")
logger.setLevel(logging.INFO)

# File handler
file_handler = logging.FileHandler("logs/app.log")
file_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler('logs/app.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)