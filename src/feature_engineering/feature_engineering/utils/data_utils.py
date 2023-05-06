from feature_engineering.params import ProgramParams

from typing import Tuple
import numpy as np

def count_positive_and_negative_labels(labels: np.ndarray) -> Tuple[int, int]:
    """
    Count the number of positive and negative labels.
    """
    nb_positive_labels = np.count_nonzero(labels)
    nb_negative_labels = len(labels) - nb_positive_labels

    return nb_positive_labels, nb_negative_labels

def log_positive_and_negative_labels(params: ProgramParams, labels: np.ndarray, message: str = "") -> None:
    nb_positive_labels, nb_negative_labels = count_positive_and_negative_labels(labels)

    if message != "":
        params.RESULTS_LOGGER.info(message)

    params.RESULTS_LOGGER.info(f'Number of positive labels: {nb_positive_labels}')
    params.RESULTS_LOGGER.info(f'Number of negative labels: {nb_negative_labels}')