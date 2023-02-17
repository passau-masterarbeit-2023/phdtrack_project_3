from .ml_utils import get_name_for_feature_and_label_save_file
from .ml_data_manips import get_samples_and_labels, load_model, oversample_using_smote, undersample_using_random_undersampler
from .ml_evaluate import evaluate
from ..params import ProgramParams
from .ml_train import train_high_recall_classifier, train_rfc

from enum import Enum

import os
import glob

class BalancingType(Enum):
    NONE = 0
    OVER = 1
    UNDER = 2

class ModelType(Enum):
    RFC = 0
    GridSearchCV = 1


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
    
    def training_pipeline(
            self, 
            modelType : ModelType, 
            balancingType : BalancingType, 
            training_dir_path: str
    ):
        """
        Training pipeline.
        """
        # get all nested .raw files
        heap_dump_raw_files = self.__get_all_nested_files(training_dir_path, "raw")

        # generate save file name
        # get last 4 filepath components
        samples_and_labels_save_file_name = get_name_for_feature_and_label_save_file(
            self.params,
            "training",
            training_dir_path
        )

        # train on each heap dump
        samples, labels = get_samples_and_labels(
            self.params,
            samples_and_labels_save_file_name,
            heap_dump_raw_files
        )
        self.__data_balancing(balancingType, samples, labels)

        return self.__train_model(modelType, balancingType, samples, labels)
    
    def testing_pipeline(
        self, 
        modelType : ModelType, 
        balancingType : BalancingType, 
        testing_dir_path: str
    ):
        """
        Testing pipeline.
        """
        # get all nested .raw files
        heap_dump_raw_files = self.__get_all_nested_files(testing_dir_path, "raw")

        # generate save file name
        # get last 4 filepath components
        samples_and_labels_save_file_name = get_name_for_feature_and_label_save_file(
            self.params,
            "testing",
            testing_dir_path
        )

        # train on each heap dump
        samples, labels = get_samples_and_labels(
            self.params,
            samples_and_labels_save_file_name,
            heap_dump_raw_files
        )

        model_name = self.__get_model_name(modelType, balancingType)

        # load model
        clf = load_model(self.params, model_name)

        return evaluate(clf, samples, labels)
    

    ############## -- logic -- #####################

    def __data_balancing(
            self, 
            balancingType : BalancingType, 
            samples : list[list[int]], 
            labels : list[int]
    ):
        """
        Data balancing.
        """
        if balancingType == BalancingType.NONE:
            return samples, labels
        elif balancingType == BalancingType.OVER:
            return oversample_using_smote(samples, labels)
        elif balancingType == BalancingType.UNDER:
            return undersample_using_random_undersampler(samples, labels)
        else:
            raise Exception("Unknown balancing type.")
        
    def __get_model_name(self, modelType : ModelType, balancingType : BalancingType):
        """
        Get model name.
        """
        if modelType == ModelType.RFC:
            return "random_forest_classifier_1_depth_{}_balancing_{}".format(
                self.params.BASE_EMBEDDING_DEPTH,
                balancingType.name
            )
        elif modelType == ModelType.GridSearchCV:
            return "grid_search_cv_1_depth_{}_balancing_{}".format(
                self.params.BASE_EMBEDDING_DEPTH,
                balancingType.name
            )
        else:
            raise Exception("Unknown model type.")
        
    def __train_model(
            self, 
            modelType : ModelType, 
            balancingType : BalancingType,
            samples : list[list[int]], 
            labels : list[int]
    ):
        """
        Train model.
        """
        if modelType == ModelType.RFC:
            return train_rfc(
                self.params, 
                self.__get_model_name(modelType, balancingType), 
                samples, 
                labels
            )
        elif modelType == ModelType.GridSearchCV:
            return train_high_recall_classifier(
                self.params, 
                self.__get_model_name(modelType, balancingType), 
                samples, 
                labels
            )
        else:
            raise Exception("Unknown model type.")
        