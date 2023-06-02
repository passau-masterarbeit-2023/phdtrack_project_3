import csv
from datetime import datetime
import os
from typing import Optional
from feature_engineering.common import BaseResultWriter

from feature_engineering.utils.utils import datetime2str

class ClassificationResultsWriter(BaseResultWriter):
    """
    This class is used to write the results of a classification pipeline to a CSV file.
    It keeps track of the headers of the CSV file and the results to write.
    It stores everything related to classification results.
    """
    more_headers: list[str] = [
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

    def __init__(self, csv_file_path: str, pipeline_name: str):
        super().__init__(csv_file_path, self.more_headers)
        self.set_result("pipeline_name", pipeline_name)

        # start time
        self.set_result("start_time", datetime2str(datetime.now()))
