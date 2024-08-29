# Flight Data Generation and Analysis

This project is designed to simulate and analyze flight data between various cities, focusing on efficient data generation, processing, and analysis techniques.

## Project Structure

- `flight_data_generator.py`: Generates random flight data as JSON files.
- `flight_data_processor.py`: Analyzes the generated data and provides insights.
- `README.md`: This file.

## Requirements

- **Python 3.8+**

## Dependencies

#### Install the required libraries:

To install the required libraries, use the following command:

``` bash
pip install -r requirements.txt
```


## Usage
####  Data Generation
Run the following command to generate flight data:


``` bash 
python flight_data_generator.py
```

#### Data Analysis

``` bash
python flight_data_processor.py
```

#### Configuration
The project uses a config.py file to manage configuration settings:

* **NUM_FILES** : Number of files to generate.
* **NUM_CITIES**: Number of cities to include in the data.
* **NULL_PROBABILITY**: Probability for NULL values in the flight data.
* **MAX_NUM_CITIES**: Maximum number of random cities to generate.
* **SINGLE_FILE_MIN_RECORDS**: Minimum number of records per file.
* **SINGLE_FILE_MAX_RECORDS**: Maximum number of records per file.
* **BASE_DIR**: Directory where flight data files are saved.
* **REPORT_DIR**: Directory where analysis reports are saved.
* **RANDOM_SEED**: Seed for random number generation to ensure reproducibility.
* **NUM_OF_TOP_DESTINATIONS_TO_REPORT**: Number of top destinations to include in the report.
* **PERCENTILE**: Percentile for flight duration analysis.


#### NOTES

* The data is randomly generated with some NULL values to simulate dirty data.
* Adjust the configuration settings in config.py as needed.

