from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score
from imblearn.under_sampling import RandomUnderSampler
import pandas as pd

from feature_engineering.data_loading.data_types import DataGenerator, DataTuple, SamplesAndLabelsType, is_datagenerator, is_datatuple
from feature_engineering.data_loading.data_loading import consume_data_generator
from feature_engineering.params.params import ProgramParams

def __ml_sgd_pipeline(params: ProgramParams, samples: pd.DataFrame, labels: pd.Series) -> None:
    """
    Pipeline for SGDClassifier with undersampling.
    """
    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(samples, labels, test_size=0.2, random_state=42)

    # Perform undersampling on the majority class
    #rus = RandomUnderSampler(random_state=42)
    #X_res, y_res = rus.fit_resample(X_train, y_train)
    X_res = X_train
    y_res = y_train

    # Train a SGDClassifier
    print(params.MAX_ML_WORKERS)
    clf = SGDClassifier(random_state=42, n_jobs = params.MAX_ML_WORKERS)

    # Train classifier
    clf.fit(X_res, y_res)

    # Make predictions on the test set
    y_pred = clf.predict(X_test)

    # Compute metrics
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    # Log the results
    params.RESULTS_LOGGER.info(f'Precision: {precision}, Recall: {recall}, F1-score: {f1}')


def __ml_sgd_pipeline_partial_fit(params: ProgramParams, samples_and_labels: SamplesAndLabelsType) -> None:
    # Train a SGDClassifier
    clf = SGDClassifier(random_state=42)
    X_test_all = pd.DataFrame()
    y_test_all = pd.Series()
    
    for samples, labels in samples_and_labels:
        # Split into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(samples, labels, test_size=0.2, random_state=42)
        X_test_all = pd.concat([X_test_all, X_test])
        y_test_all = pd.concat([y_test_all, y_test])

        # Perform undersampling on the majority class
        rus = RandomUnderSampler(random_state=42)
        X_res, y_res = rus.fit_resample(X_train, y_train)

        # Here classes=[0, 1] as we are assuming binary classification
        clf.partial_fit(X_res, y_res, classes=[0, 1])

    # Make predictions on the test set
    y_pred = clf.predict(X_test_all)

    # Compute metrics
    precision = precision_score(y_test_all, y_pred)
    recall = recall_score(y_test_all, y_pred)
    f1 = f1_score(y_test_all, y_pred)

    # Log the results
    params.RESULTS_LOGGER.info(f'Precision: {precision}, Recall: {recall}, F1-score: {f1}')



def ml_sgd_pipeline(params: ProgramParams, samples_and_labels: SamplesAndLabelsType, partial_fit: bool = False) -> None:

    if is_datatuple(samples_and_labels):
        # check the samples and labels
        samples, labels = samples_and_labels
        __ml_sgd_pipeline(params, samples, labels)
    elif is_datagenerator(samples_and_labels):
        __ml_sgd_pipeline_partial_fit(params, samples_and_labels)
    else:
        raise TypeError(f"Invalid type for samples_and_labels: {type(samples_and_labels)}")
