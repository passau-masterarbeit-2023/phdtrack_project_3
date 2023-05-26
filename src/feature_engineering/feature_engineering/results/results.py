import csv
from datetime import datetime
import os
from typing import Optional

from feature_engineering.utils.utils import datetime2str

class ClassificationResultsWriter:
    """
    This class is used to write the results of a classification pipeline to a CSV file.
    It keeps track of the headers of the CSV file and the results to write.
    It stores everything related to classification results.
    """
    csv_file_path: str
    headers: list[str] = [
        "pipeline_name", 
        "start_time", 
        "end_time", 
        "duration",
        "data_loading_duration", 
        "data_processing_duration", 
        "model_type",
        "balancing_type", 
        "training_dataset_origin", 
        "testing_dataset_origin",
        "nb_training_samples_before_balancing",
        "nb_positive_training_samples_before_balancing",
        "nb_training_samples_after_balancing",
        "nb_positive_training_samples_after_balancing", 
        "precision",
        "recall", 
        "f1_score", 
        "support", 
        "true_positives", 
        "true_negatives",
        "false_positives", 
        "false_negatives", 
        "auc"
    ]
    results: dict[str, Optional[str]]

    def __init__(self, csv_file_path: str, pipeline_name: str):
        self.csv_file_path = csv_file_path
        self.results = {header: None for header in self.headers}

        self.set_result("pipeline_name", pipeline_name)

        # start time
        self.set_result("start_time", datetime2str(datetime.now()))
        
    def set_result(self, field: str, value: Optional[str]) -> None:
        if field in self.results:
            self.results[field] = value
        else:
            raise ValueError(f"ClassificationResultsWriter: Invalid field name: {field}")
        
    def write_results(self) -> None:
        file_exists = os.path.isfile(self.csv_file_path)
        with open(self.csv_file_path, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            if not file_exists:
                writer.writeheader()
            writer.writerow(self.results)
    
    def print_results(self) -> None:
        for key, value in self.results.items():
            print(f"{key}: {value}")
