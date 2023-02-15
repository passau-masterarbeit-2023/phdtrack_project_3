

from ..params import ProgramParams
from .ml_trainer import MLTrainer

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
    
    def training_pipeline(self):
        """
        Training pipeline.
        """
        # get all nested .raw files
        heap_dump_raw_files = self.__get_all_nested_files(
            self.params.DATA_DIR_PATH, "raw"
        )

        # train on each heap dump
        ml_trainer = MLTrainer(self.params)
        ml_trainer.train(heap_dump_raw_files)