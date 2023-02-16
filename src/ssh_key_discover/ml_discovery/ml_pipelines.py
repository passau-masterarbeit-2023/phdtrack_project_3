from .ml_data_manips import get_samples_and_labels
from ..params import ProgramParams
from .ml_train import train_rfc

import os
import glob

class Pipelines():
    params: ProgramParams

    def __init__(self, params: ProgramParams):
        self.params = params
    
    def __get_all_nested_files(self, dir_path: str, extension: str | None = None) -> list[str]:
        """
        Get all nested files in a directory.
        """
        # use glob to get all files
        all_files: list[str]
        if extension is None:
            all_files = glob.glob(os.path.join(dir_path, "**"), recursive=True)
        else:
            all_files = glob.glob(os.path.join(dir_path, "**", f"*.{extension}"), recursive=True)
        
        # filter out directories
        all_files = [file for file in all_files if os.path.isfile(file)]

        return all_files
    
    def training_pipeline(self, model_name: str, training_dir_path: str):
        """
        Training pipeline.
        """
        # get all nested .raw files
        heap_dump_raw_files = self.__get_all_nested_files(training_dir_path, "raw")

        # generate save file name
        # get last 4 filepath components
        filepath_components = training_dir_path.split(os.sep)
        filepath_components = filepath_components[-4:]
        samples_and_labels_save_file_name = "samples_and_labels_training__{}.pkl".format(
            "_".join(filepath_components)
        )

        # train on each heap dump
        samples, labels = get_samples_and_labels(
            self.params,
            samples_and_labels_save_file_name,
            heap_dump_raw_files
        )

        return train_rfc(self.params, model_name, samples, labels)