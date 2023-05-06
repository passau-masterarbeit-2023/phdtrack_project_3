from concurrent.futures import ThreadPoolExecutor
import glob
from typing import Tuple
import numpy as np
import os

from feature_engineering.params import ProgramParams

def load_samples_and_labels_from_csv(csv_file_path: str) -> Tuple[np.ndarray, np.ndarray] | None:
    # Load the data from the CSV file
    data = np.genfromtxt(csv_file_path, delimiter=',', skip_header=1)

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

            check_samples_and_labels(params, samples, labels)

            if all_samples is None and all_labels is None:
                all_samples = samples
                all_labels = labels
            else:
                all_samples = np.concatenate((all_samples, samples))
                all_labels = np.concatenate((all_labels, labels))

    params.COMMON_LOGGER.info(f'Number of empty files: {len(list_of_empty_files)}')

    return all_samples, all_labels


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

    def load_samples_and_labels_from_csv_and_concatenate(
            csv_file_path: str, 
            threadId: int, 
            nb_threads: int
        ) -> None:
        """
        Load the samples and labels from one .csv file.
        """
        params.RESULTS_LOGGER.info(f"[{threadId}/{nb_threads}] Loading samples and labels from {csv_file_path}")

        res = load_samples_and_labels_from_csv(csv_file_path)
        if res is None:
            list_of_empty_files.append(csv_file_path)
        else:
            samples, labels = res

            # Print the shapes of the arrays
            params.COMMON_LOGGER.debug(f'shape of samples: {samples.shape}, shape of labels: {labels.shape}')

            check_samples_and_labels(params, samples, labels)

            nonlocal all_samples
            nonlocal all_labels

            if all_samples is None and all_labels is None:
                all_samples = samples
                all_labels = labels
            else:
                all_samples = np.concatenate((all_samples, samples))
                all_labels = np.concatenate((all_labels, labels))

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

    training_files = [file for file in all_files if "training" in file.lower()]
    validation_files = [file for file in all_files if "validation" in file.lower()]
    testing_files = [file for file in all_files if "performance_test" in file.lower()]
        
    return training_files, validation_files, testing_files


def check_samples_and_labels(params: ProgramParams, samples: np.ndarray, labels: np.ndarray):
    """
    Check that the samples and labels are valid.
    """
    # check that the number of samples and labels is the same
    assert samples.shape[0] == labels.shape[0], "The number of samples and labels is not the same."
    # check that the number of features is the same for all samples
    assert len(set(samples.shape[1:])) == 1, "The number of features is not the same for all samples."
    # check that the labels are either 0 or 1
    assert set(labels) == {0, 1}, "The labels are not either 0 or 1."
    # check that labels are not all the same
    assert len(set(labels)) > 1, "The labels are all the same."
    # check that the samples are not all the same
    unique_samples = np.unique(samples, axis=0)
    assert unique_samples.shape[0] > 1, "The samples are all the same."

    # log that the samples and labels have been checked
    params.COMMON_LOGGER.info(f"✅ Checked samples and labels.")
