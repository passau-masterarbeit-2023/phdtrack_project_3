

import csv
import os
from typing import Optional


class BaseResultWriter(object):
    """
    This class is used to write the results to a CSV file.
    It keeps track of the headers of the CSV file and the results to write.
    It stores everything related to the results.
    """
    csv_file_path: str
    headers: list[str] = [
        "pipeline_name", 
        "start_time", 
        "end_time", 
        "duration",
    ]
    results: dict[str, Optional[str]]

    def __init__(self, csv_file_path: str, more_header: list[str]):
        self.csv_file_path = csv_file_path
        self.headers += more_header
        self.results = {header: None for header in self.headers + more_header}


    def set_result(self, field: str, value: Optional[str]) -> None:
        if field in self.results:
            self.results[field] = value
        else:
            raise ValueError(f"ClassificationResultsWriter: Invalid field name: {field}")
        
    def write_results(self) -> None:
        file_exists = os.path.isfile(self.csv_file_path)
        with open(self.csv_file_path, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            # write header only if file is empty or does not exist
            if not file_exists or os.stat(self.csv_file_path).st_size == 0:
                writer.writeheader()
            writer.writerow(self.results)
    
    def print_results(self) -> None:
        for key, value in self.results.items():
            print(f"{key}: {value}")
    