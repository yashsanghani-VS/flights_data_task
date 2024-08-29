import random
from pathlib import Path

# Configuration settings for the flight data generator and processor

class Config:
    # Flight generation settings
    NUM_FILES = 5000
    NUM_CITIES = random.randint(100, 200)
    CITY_LIST = []
    NULL_PROBABILITY = random.uniform(0.005, 0.001)  # probability for NULL values

    # Maximum number of random cities to generate
    MAX_NUM_CITIES = 400
    
    # Flight data settings for single json file
    SINGLE_FILE_MIN_RECORDS = 50
    SINGLE_FILE_MAX_RECORDS = 100
    
    # File paths
    BASE_DIR = Path('tmp/flights')
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR = Path('clean_data')
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    # Random seed for reproducibility
    RANDOM_SEED = 42
    
    # Flight data processing settings
    NUM_OF_TOP_DESTINATIONS_TO_REPORT = 30
    
    # Percentile for flight duration analysis
    PERCENTILE = 90
