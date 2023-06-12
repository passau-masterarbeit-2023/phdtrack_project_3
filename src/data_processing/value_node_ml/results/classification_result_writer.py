from datetime import datetime
from commons.results.base_result_writer import BaseResultWriter

from commons.utils.utils import datetime2str
from value_node_ml.params.pipeline_params import PipelineNames

class ClassificationResultsWriter(BaseResultWriter):
    """
    This class is used to write the results of a classification pipeline to a CSV file.
    It keeps track of the headers of the CSV file and the results to write.
    It stores everything related to classification results.
    """
    ADDITIONAL_HEADERS: list[str] = [
        "data_loading_duration", 
        "data_balancing_duration",
        "balancing_type", 
        "model_name",
        "training_dataset_origin", 
        "testing_dataset_origin",
        "nb_training_samples_before_balancing",
        "nb_positive_training_samples_before_balancing",
        "nb_training_samples_after_balancing",
        "nb_positive_training_samples_after_balancing", 
        "precision",
        "recall", 
        "accuracy",
        "f1_score", 
        "support", 
        "true_positives", 
        "true_negatives",
        "false_positives", 
        "false_negatives", 
        "auc"
    ]

    def __init__(self, csv_file_path: str, pipeline_name: PipelineNames):
        super().__init__(csv_file_path, self.ADDITIONAL_HEADERS, pipeline_name)
