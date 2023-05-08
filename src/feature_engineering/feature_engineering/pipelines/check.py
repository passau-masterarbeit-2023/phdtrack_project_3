import numpy as np
from feature_engineering.utils.utils import time_measure
from feature_engineering.params.params import ProgramParams

def __check_samples_and_labels(params: ProgramParams, samples: np.ndarray, labels: np.ndarray):
    """
    Check that the samples and labels are valid.
    """
    # Check if samples is a 2D NumPy array
    assert len(samples.shape) == 2, "samples is not a 2D NumPy array."

    # check that the number of samples and labels is the same
    assert samples.shape[0] == labels.shape[0], "The number of samples ({}) and labels ({}) is not the same.".format(
        samples.shape[0], labels.shape[0]
    )

    # Check if arrays are of type integer
    assert labels.dtype == np.int32, "labels is not an array of integers."
    assert samples.dtype == np.int32, "samples is not an array of integers."

    # Check that the arrays don't contain invalid values
    assert not np.any(np.isnan(samples)), "The array 'samples' contains NaN values."
    assert not np.any(np.isinf(samples)), "The array 'samples' contains infinity values."
    assert not np.any(np.isnan(labels)), "The array 'labels' contains NaN values."
    assert not np.any(np.isinf(labels)), "The array 'labels' contains infinity values."

    # check that the labels are either 0 or 1
    assert np.all(np.isin(labels, [0, 1])), "The labels are not either 0 or 1."
    
    # check that labels are not all the same
    assert len(set(labels)) > 1, "The labels are all the same."
    # check that the samples are not all the same
    unique_samples = np.unique(samples, axis=0)
    assert unique_samples.shape[0] > 1, "The samples are all the same."

    # log that the samples and labels have been checked
    params.COMMON_LOGGER.info(f"✅ Checked samples and labels.")


def check(params: ProgramParams, samples: np.ndarray, labels: np.ndarray) -> None:
    """
    Pipeline for checking the samples and labels.
    """

    # check the samples and labels
    with time_measure(f'check pipeline: ', params.RESULTS_LOGGER):
        __check_samples_and_labels(params, samples, labels)

