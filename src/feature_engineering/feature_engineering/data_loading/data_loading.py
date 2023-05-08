from concurrent.futures import ThreadPoolExecutor
import glob
from typing import Tuple
import numpy as np
import os

from feature_engineering.utils.data_utils import count_positive_and_negative_labels
from feature_engineering.params.data_origin import DataOriginEnum
from feature_engineering.utils.utils import time_measure
from feature_engineering.params.params import ProgramParams

def load_samples_and_labels_from_csv(csv_file_path: str) -> Tuple[np.ndarray, np.ndarray] | None:
    # Load the data from the CSV file
    data = np.genfromtxt(
        csv_file_path, 
        delimiter=',', 
        skip_header=1,
        dtype=np.int32,  # enforce int32 data type
    )

    # check if data is empty
    if data.size == 0:
        return None

    try:
        # Extract the labels from the last column
        labels = data[:, -1]

        # Extract the samples from the other columns
        samples = data[:, :-1]

    except Exception as e:
        raise type(e)(e.__str__() + f". Error loading data from {csv_file_path}")

    return samples, labels


def load_samples_and_labels_from_all_csv_files(
        params: ProgramParams, csv_file_paths: list[str]
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Load the samples and labels from all .csv files.
    """
    # stats
    list_of_empty_files = []

    all_samples: np.ndarray | None = None
    all_labels: np.ndarray | None = None

    for i in range(len(csv_file_paths)):
        csv_file_path = csv_file_paths[i]

        # log the current file with respect to the total number of files
        params.COMMON_LOGGER.info(f'📋 [f: {i} / {len(csv_file_paths)}] Loading file {csv_file_path} ')

        res = load_samples_and_labels_from_csv(csv_file_path)
        if res is None:
            list_of_empty_files.append(csv_file_path)
        else:
            samples, labels = res

            # Print the shapes of the arrays
            params.COMMON_LOGGER.debug(f'shape of samples: {samples.shape}, shape of labels: {labels.shape}')

            if all_samples is None and all_labels is None:
                all_samples = samples
                all_labels = labels
            else:
                all_samples = np.concatenate((all_samples, samples))
                all_labels = np.concatenate((all_labels, labels))

    params.COMMON_LOGGER.info(f'Number of empty files: {len(list_of_empty_files)}')

    return all_samples, all_labels


from concurrent.futures import ThreadPoolExecutor
from threading import Lock
import numpy as np
from typing import Tuple

def parallel_load_samples_and_labels_from_all_csv_files(
        params: ProgramParams, csv_file_paths: list[str]
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Load the samples and labels from all .csv files.
    Load using multiple threads.
    """
    # stats
    list_of_empty_files = []

    all_samples: np.ndarray | None = None
    all_labels: np.ndarray | None = None

    # Define a lock for thread safety
    concat_lock = Lock()

    def load_samples_and_labels_from_csv_and_concatenate(
            csv_file_path: str, 
            threadId: int, 
            nb_threads: int
        ) -> None:
        """
        Load the samples and labels from one .csv file.
        """
        params.RESULTS_LOGGER.info(f"📋 [{threadId}/{nb_threads}] Loading samples and labels from {csv_file_path}")

        res = load_samples_and_labels_from_csv(csv_file_path)
        if res is None:
            list_of_empty_files.append(csv_file_path)
        else:
            samples, labels = res

            # Print the shapes of the arrays
            params.COMMON_LOGGER.debug(f'shape of samples: {samples.shape}, shape of labels: {labels.shape}')

            nonlocal all_samples
            nonlocal all_labels

            # Acquire the lock
            with concat_lock:
                if all_samples is None and all_labels is None:
                    all_samples = samples
                    all_labels = labels
                else:
                    all_samples = np.concatenate((all_samples, samples))
                    all_labels = np.concatenate((all_labels, labels))
            # The lock is released after the 'with' statement

    # multi-threaded loading and generation of samples and labels
    with ThreadPoolExecutor(max_workers=min(params.MAX_ML_WORKERS, 6)) as executor:
        results = executor.map(
            load_samples_and_labels_from_csv_and_concatenate, 
            csv_file_paths,
            range(len(csv_file_paths)),
            [len(csv_file_paths)] * len(csv_file_paths)
        )
        for _ in results:
            pass

    params.COMMON_LOGGER.info(f'Number of empty files: {len(list_of_empty_files)}')

    return all_samples, all_labels



def get_all_filepath_per_type(dirpath: str) -> Tuple[list[str], list[str], list[str]]:
    """
    Determine the filepaths for all data .csv files inside the directory.
    Return the filepaths for the training, validation, and testing data.
    """
    extension = "csv"
    all_files = glob.glob(os.path.join(dirpath, "**", f"*.{extension}"), recursive=True)

    training_files = [file for file in all_files if DataOriginEnum.Training in file.lower()]
    validation_files = [file for file in all_files if DataOriginEnum.Validation in file.lower()]
    testing_files = [file for file in all_files if DataOriginEnum.Testing in file.lower()]
        
    return training_files, validation_files, testing_files


def log_positive_and_negative_labels(params: ProgramParams, labels: np.ndarray, message: str = "") -> None:
    nb_positive_labels, nb_negative_labels = count_positive_and_negative_labels(labels)

    if message != "":
        params.RESULTS_LOGGER.info(message)

    params.RESULTS_LOGGER.info(f'Number of positive labels: {nb_positive_labels}')
    params.RESULTS_LOGGER.info(f'Number of negative labels: {nb_negative_labels}')


def load(
        params: ProgramParams, 
        data_dir_path: str, 
        data_origin: set[DataOriginEnum] | None = None
):
    """
    Load the samples and labels from all .csv files.
    Take into account the data origin: training, validation, testing.
    If data_origin is None, load all data.
    """
    
    # Get the filepaths for the training, validation, and testing data
    training_files, validation_files, testing_files = get_all_filepath_per_type(data_dir_path)

    files_to_load = []
    if data_origin is None:
        files_to_load = training_files + validation_files + testing_files
    else:
        for origin in data_origin:
            if origin == DataOriginEnum.Training:
                files_to_load += training_files
            elif origin == DataOriginEnum.Validation:
                files_to_load += validation_files
            elif origin == DataOriginEnum.Testing:
                files_to_load += testing_files
            else:
                raise ValueError(f"Unknown data origin: {origin}")

    # Load the training data
    with time_measure(f'load_samples_and_labels_from_all_csv_files', params.RESULTS_LOGGER):
        #training_samples, training_labels = load_samples_and_labels_from_all_csv_files(params, training_files)
        samples, labels = parallel_load_samples_and_labels_from_all_csv_files(params, files_to_load)

    log_positive_and_negative_labels(
        params, 
        labels, 
        "Loaded data ({})".format(", ".join(data_origin).replace(" ", ""))
    )

    return samples, labels