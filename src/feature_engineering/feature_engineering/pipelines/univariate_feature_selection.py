import numpy as np
from feature_engineering.params.params import ProgramParams

def __compute_distance_f_test_p_val(f_values: np.ndarray, p_values: np.ndarray) -> float:
    """
    Compute the distance between the F-test value and the p-value.
    """
    # we need to linearize the F-test value and the p-value
    # because they have different scales
    # we want to compute the distance between the two values
    # so we need to linearize them
    f_val_min, f_val_max = np.min(f_values), np.max(f_values)
    p_val_min, p_val_max = np.min(p_values), np.max(p_values)

    # bring p_values to the same scale as f_values
    f_values_coef = (f_val_max - f_val_min) / (p_val_max - p_val_min)
    p_values = p_values * f_values_coef

    ponderated_values = f_values - p_values
    print("f_values: ",f_values)
    print("p_values: ",p_values)
    print("ponderated_values: ",ponderated_values)

    # sorting values considering the F-test value (descending) and the p-value (ascending)
    sorted_indices = np.argsort(ponderated_values)
    return sorted_indices


def __compute_distance_f_test_p_val_2(f_values: np.ndarray, p_values: np.ndarray) -> np.ndarray:
    """
    Compute the distance between the F-test value and the p-value.
    """
    # Normalize F-test values and p-values to the range [0, 1]
    f_values_norm = (f_values - np.min(f_values)) / (np.max(f_values) - np.min(f_values))
    p_values_norm = (p_values - np.min(p_values)) / (np.max(p_values) - np.min(p_values))

    # Compute the combined importance value for each feature
    combined_values = f_values_norm - p_values_norm
    print("f_values_norm: ", f_values_norm)
    print("p_values_norm: ", p_values_norm)
    print("combined_values: ", combined_values)

    # Sort the features based on the combined importance values (descending)
    sorted_indices = np.argsort(-combined_values)
    return sorted_indices

    

def univariate_feature_selection_pipeline(params: ProgramParams, samples: np.ndarray, labels: np.ndarray) -> None:
    """
    Pipeline for univariate feature selection.
    """
    # feature selection
    from sklearn.feature_selection import SelectKBest, f_classif
    selector = SelectKBest(f_classif, k=10)
    res = selector.score_func(samples, labels)
    print(res)

    # feature ranking
    # Replace nan values with the maximum possible float value to ensure they are ranked last
    f_values, p_values = res
    p_values_no_nan = np.where(np.isnan(p_values), np.finfo(np.float64).max, p_values)

    # Sort the features based on F-statistic values (descending) and p-values (ascending)
    #sorted_indices = np.lexsort((-f_values, p_values_no_nan))
    sorted_indices = __compute_distance_f_test_p_val_2(f_values, p_values)

    # Print the sorted feature indices
    print("Feature indices sorted by importance:")
    print("sorted indices (features): ", ", ".join([str(i) for i in sorted_indices]))

    #selector.fit(training_samples, training_labels)
    #X_new = selector.transform(training_samples)


