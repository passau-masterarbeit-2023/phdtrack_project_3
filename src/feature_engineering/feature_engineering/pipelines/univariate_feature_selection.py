from feature_engineering.data_loading.data_loading import get_all_filepath_per_type, load_samples_and_labels_from_all_csv_files, parallel_load_samples_and_labels_from_all_csv_files
from feature_engineering.utils.utils import time_measure
from feature_engineering.utils.data_utils import log_positive_and_negative_labels
from feature_engineering.params import ProgramParams

def univariate_feature_selection_pipeline(params: ProgramParams, data_dir_path: str) -> None:
    """
    Pipeline for univariate feature selection.
    """
    # Get the filepaths for the training, validation, and testing data
    training_files, validation_files, testing_files = get_all_filepath_per_type(data_dir_path)

    # Load the training data
    with time_measure(f'load_samples_and_labels_from_all_csv_files', params.RESULTS_LOGGER):
        #training_samples, training_labels = load_samples_and_labels_from_all_csv_files(params, training_files)
        training_samples, training_labels = parallel_load_samples_and_labels_from_all_csv_files(params, testing_files)

    log_positive_and_negative_labels(params, training_labels, "Training data: ")

    # feature selection
    from sklearn.feature_selection import SelectKBest, f_classif
    selector = SelectKBest(f_classif, k=10)
    res = selector.score_func(training_samples, training_labels)
    print(res)

    #selector.fit(training_samples, training_labels)
    #X_new = selector.transform(training_samples)


