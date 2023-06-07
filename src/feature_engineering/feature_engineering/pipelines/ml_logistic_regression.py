from typing import Optional
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, precision_score, recall_score

from feature_engineering.data_loading.data_types import SamplesAndLabels, SamplesAndLabelsUnion
from feature_engineering.pipelines.pipeline_utils import handle_data_origin_consume_generator
from feature_engineering.params.data_origin import DataOriginEnum
from feature_engineering.pipelines.univariate_feature_selection import __compute_distance_f_test_p_val
from feature_engineering.params.params import ProgramParams

def __ml_logistic_regression_pipeline(
        params: ProgramParams, 
        samples_and_labels_train: SamplesAndLabels,
        samples_and_labels_test: Optional[SamplesAndLabels],
    ) -> None:

    if samples_and_labels_test is None:
        # Split data into training and test sets
        __samples, __labels = samples_and_labels_train
        X_train, X_test, y_train, y_test = train_test_split(__samples, __labels, test_size=0.2, random_state=42)
    else:
        X_train, y_train = samples_and_labels_train
        X_test, y_test = samples_and_labels_test

    # Feature selection
    selector = SelectKBest(f_classif, k=10)
    X_train_transformed = selector.fit_transform(X_train, y_train)

    # log selected features
    column_names_after_selection = X_train.columns[selector.get_support()].tolist()
    params.RESULTS_LOGGER.info(f'Selected features: {column_names_after_selection}')

    f_values, p_values = selector.score_func(X_train, y_train)
    column_names = X_train.columns.tolist()

    # Train classifier
    clf = LogisticRegression(n_jobs = params.MAX_ML_WORKERS)
    clf.fit(X_train_transformed, y_train)

    # Apply feature selection to test set
    X_test_transformed = selector.transform(X_test)

    # Predict labels for test set
    y_pred = clf.predict(X_test_transformed)

    # Evaluate model
    f1 = f1_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)

    params.RESULTS_LOGGER.info(f'F1 score: {f1}')
    params.RESULTS_LOGGER.info(f'Precision: {precision}')
    params.RESULTS_LOGGER.info(f'Recall: {recall}')

    # Return feature importance
    f_values, p_values = selector.score_func(X_train, y_train)
    sorted_indices = __compute_distance_f_test_p_val(f_values, p_values)
    sorted_column_names = [column_names[i] for i in sorted_indices]
    params.RESULTS_LOGGER.info(f"Column names sorted by importance: [{', '.join(sorted_column_names)}]")


def ml_logistic_regression_pipeline(
        params: ProgramParams, 
        origin_to_samples_and_labels: dict[DataOriginEnum, SamplesAndLabelsUnion]
    ) -> None:
    """
    Pipeline for training a logistic regression model.
    """

    samples_and_labels_train: SamplesAndLabels 
    samples_and_labels_test: Optional[SamplesAndLabels] = None

    samples_and_labels_train = handle_data_origin_consume_generator(
        params.data_origins_training,
        origin_to_samples_and_labels
    )
    if params.data_origins_testing is not None:
        samples_and_labels_test = handle_data_origin_consume_generator(
            params.data_origins_testing,
            origin_to_samples_and_labels
        )
    
    # launch the pipeline
    __ml_logistic_regression_pipeline(params, samples_and_labels_train, samples_and_labels_test)
