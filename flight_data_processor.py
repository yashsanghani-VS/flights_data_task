import time
import os
import json
import logging
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
from typing import Tuple, Dict, List
import numpy as np
from config import Config

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FlightDataProcessor:
    """Class responsible for processing and analyzing flight data."""

    def __init__(self, config: Config):
        self.config = config

    def _process_single_file(self, file_path: str) -> Tuple[int, int, Dict[str, List[int]], Dict[str, int], Dict[str, int]]:
        record_count = 0
        dirty_record_count = 0
        destination_city_durations = defaultdict(list)
        city_passengers_arrived = defaultdict(int)
        city_passengers_left = defaultdict(int)

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                for record in data:
                    record_count += 1
                    if None in record.values():
                        dirty_record_count += 1
                    else:
                        destination_city_durations[record["destination_city"]].append(record["flight_duration_secs"])
                        city_passengers_arrived[record["destination_city"]] += record["passengers_on_board"]
                        city_passengers_left[record["origin_city"]] += record["passengers_on_board"]
        except Exception as e:
            logging.error(f"Error processing file {file_path}: {e}")
        
        return record_count, dirty_record_count, destination_city_durations, city_passengers_arrived, city_passengers_left

    def process_all_files(self):
        """Processes all flight data files and outputs analysis results."""
        start_time = time.time()
        total_record_count = 0
        total_dirty_record_count = 0
        destination_city_durations = defaultdict(list)
        city_passengers_arrived = defaultdict(int)
        city_passengers_left = defaultdict(int)

        files = [os.path.join(root, file) for root, _, files in os.walk(self.config.BASE_DIR) for file in files]

        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(self._process_single_file, file) for file in files]
            for future in as_completed(futures):
                result = future.result()
                total_record_count += result[0]
                total_dirty_record_count += result[1]
                for city, durations in result[2].items():
                    destination_city_durations[city].extend(durations)
                for city, passengers in result[3].items():
                    city_passengers_arrived[city] += passengers
                for city, passengers in result[4].items():
                    city_passengers_left[city] += passengers

        self._generate_report(
            total_record_count, total_dirty_record_count,
            destination_city_durations, city_passengers_arrived, city_passengers_left, start_time
        )

    def _generate_report(
        self, total_records: int, dirty_records: int,
        destination_city_durations: Dict[str, List[int]], city_passengers_arrived: Dict[str, int],
        city_passengers_left: Dict[str, int], start_time: float
    ):
        """Generates and saves the analysis report."""
        top_no_of_destinations = sorted(
            destination_city_durations.keys(), key=lambda city: len(destination_city_durations[city]), reverse=True
        )[:self.config.NUM_OF_TOP_DESTINATIONS_TO_REPORT]

        avg_durations = {}
        percentile_durations = {}
        for city in top_no_of_destinations:
            durations = destination_city_durations[city]
            avg_durations[city] = np.mean(durations)
            percentile_durations[city] = np.percentile(durations, self.config.PERCENTILE)
        
        try:
            if not city_passengers_arrived:
                raise ValueError("No data available for city_passengers_arrived.")
            max_passengers_arrived_city = max(city_passengers_arrived, key=city_passengers_arrived.get)
        except ValueError as e:
            logging.error(f"Error determining city with max passengers arrived: {e}")
            max_passengers_arrived_city = "N/A"

        try:
            if not city_passengers_left:
                raise ValueError("No data available for city_passengers_left.")
            max_passengers_left_city = max(city_passengers_left, key=city_passengers_left.get)
        except ValueError as e:
            logging.error(f"Error determining city with max passengers left: {e}")
            max_passengers_left_city = "N/A"

        duration = time.time() - start_time
        report_content = [
            f"Total records processed: {total_records}",
            f"Dirty records: {dirty_records}",
            f"Total run duration: {duration:.2f} seconds \n",
            f"Top {self.config.NUM_OF_TOP_DESTINATIONS_TO_REPORT} Destination Cities (AVG and P95 flight duration): \n"
        ]
        for city in top_no_of_destinations:
            report_content.append(f"{city}: AVG = {avg_durations[city]}, P{self.config.PERCENTILE} = {percentile_durations[city]}")

        report_content.append(f"City with MAX passengers arrived: {max_passengers_arrived_city}")
        report_content.append(f"City with MAX passengers left: {max_passengers_left_city}")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = self.config.REPORT_DIR / f"flights_report_{timestamp}.txt"
        with open(file_name, 'w') as f:
            f.write("\n".join(report_content))

        logging.info(f"Results saved to {file_name}")

if __name__ == "__main__":
    config = Config()
    processor = FlightDataProcessor(config)
    processor.process_all_files()
