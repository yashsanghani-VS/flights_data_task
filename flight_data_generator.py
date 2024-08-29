import uuid
import json
import random
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from faker import Faker
from config import Config

class FlightDataGenerator:
    """Class responsible for generating random flight data."""

    def __init__(self, config: Config):
        self.config = config
        self.fake = Faker()
        Faker.seed(config.RANDOM_SEED)
        random.seed(config.RANDOM_SEED)
        self.config.CITY_LIST = self._generate_city_list()

    def _generate_city_list(self):
        max_num_cities = self.config.MAX_NUM_CITIES
        return list(set([self.fake.city() for _ in range(max_num_cities)]))[:self.config.NUM_CITIES]

    def _generate_random_date(self):
        start = datetime.now()
        end = start + timedelta(days=365)
        return start + (end - start) * random.random()

    def _generate_flight_data(self):
        flight_data = []
        for _ in range(random.randint(self.config.SINGLE_FILE_MIN_RECORDS, self.config.SINGLE_FILE_MAX_RECORDS)):
            flight = {
                "date": self._generate_random_date().isoformat(),
                "origin_city": random.choice(self.config.CITY_LIST),
                "destination_city": random.choice(self.config.CITY_LIST),
                "flight_duration_secs": random.randint(30 * 60, 12 * 60 * 60),
                "passengers_on_board": random.randint(1, 500),
            }
            if random.random() < self.config.NULL_PROBABILITY:
                flight[random.choice(list(flight.keys()))] = None
            flight_data.append(flight)
        return flight_data

    def _save_flight_data(self, file_name):
        with open(file_name, 'w') as f:
            json.dump(self._generate_flight_data(), f)

    def generate_files(self):
        """Generates N JSON files with random flight data."""
        month_year = datetime.now().strftime("%m-%y")
        with ThreadPoolExecutor() as executor:
            for _ in range(self.config.NUM_FILES):
                unique_id = str(uuid.uuid4().int >> 96)
                file_name = self.config.BASE_DIR / f"{month_year}-{unique_id}-flights.json"
                executor.submit(self._save_flight_data, file_name)


if __name__ == "__main__":
    config = Config()
    generator = FlightDataGenerator(config)
    generator.generate_files()
