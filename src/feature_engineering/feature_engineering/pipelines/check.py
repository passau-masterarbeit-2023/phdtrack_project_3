import numpy as np
import pandas as pd

from feature_engineering.data_loading.data_types import DataTuple, SamplesAndLabelsType, DataGenerator, is_datagenerator, is_datatuple
from feature_engineering.utils.utils import time_measure
from feature_engineering.params.params import ProgramParams

def __check_samples_and_labels(params: ProgramParams, samples: pd.DataFrame, labels: pd.Series):
    """
    Check that the samples and labels are valid.
    """
    # Check if samples is a 2D DataFrame
    assert samples.ndim == 2, "samples is not a 2D DataFrame."

    # check that the number of samples and labels is the same
    assert samples.shape[0] == labels.shape[0], "The number of samples ({}) and labels ({}) is not the same.".format(
        samples.shape[0], labels.shape[0]
    )

    # Check if arrays are of type integer
    assert pd.api.types.is_integer_dtype(labels), "labels is not a Series of integers."
    for column in samples.columns:
        assert pd.api.types.is_integer_dtype(samples[column]), f"Column '{column}' is not of type integer."

    # Check that the arrays don't contain invalid values
    assert not samples.isna().any().any(), "The DataFrame 'samples' contains NaN values."
    assert not samples.applymap(np.isinf).any().any(), "The DataFrame 'samples' contains infinity values."
    assert not labels.isna().any(), "The Series 'labels' contains NaN values."
    assert not labels.apply(np.isinf).any(), "The Series 'labels' contains infinity values."

    # check that the labels are either 0 or 1
    assert labels.isin([0, 1]).all(), "The labels are not either 0 or 1."
    
    # check that labels are not all the same
    assert labels.nunique() > 1, "The labels are all the same."
    # check that the samples are not all the same
    unique_samples = samples.drop_duplicates()
    assert unique_samples.shape[0] > 1, "The samples are all the same."

    # log that the samples and labels have been checked
    params.COMMON_LOGGER.info(f"✅ Checked samples and labels.")



def check(params: ProgramParams, samples_and_labels: SamplesAndLabelsType) -> None:
    """
    Pipeline for checking the samples and labels.
    """

    if is_datatuple(samples_and_labels):
        # check the samples and labels
        samples, labels = samples_and_labels
        __check_samples_and_labels(params, samples, labels)
    elif is_datagenerator(samples_and_labels):
        # check the samples and labels
        for samples, labels in samples_and_labels:
            __check_samples_and_labels(params, samples, labels)
    else:
        raise TypeError(f"Invalid type for samples_and_labels: {type(samples_and_labels)}")


