from typing import Optional
from feature_engineering.params.pipeline_params import PipelineNames
from .results import ClassificationResultsWriter

class ResultsManager:
    """
    Manager of different result writers (one per pipeline).
    """
    classification_result_writer_dict: dict[PipelineNames, ClassificationResultsWriter]
    csv_classification_results_path: str

    def __init__(self, csv_classification_results_path: str):
        self.csv_classification_results_path = csv_classification_results_path
        
        # result keepers
        self.__create_results_keepers()

    def __create_results_keepers(self):
        """
        Create results keepers.
        """
        self.classification_result_writer_dict = {}
        for pipeline_name in PipelineNames:
            self.classification_result_writer_dict[pipeline_name] = ClassificationResultsWriter(
                self.csv_classification_results_path,
                pipeline_name ,
            )
    
    def set_result_forall(
        self, field: str, value: Optional[str]    
    ) -> None:
        """
        Set a result for all result keepers.
        """
        for classification_result_writer in self.classification_result_writer_dict.values():
            classification_result_writer.set_result(field, value)
    
    def set_result_for(
        self, pipeline_name: PipelineNames, field: str, value: Optional[str]    
    ) -> None:
        """
        Set a result for a specific result keeper.
        """
        self.classification_result_writer_dict[pipeline_name].set_result(field, value)

    def write_results_forall(self) -> None:
        """
        Write results for all result keepers.
        """
        for classification_result_writer in self.classification_result_writer_dict.values():
            classification_result_writer.write_results()

