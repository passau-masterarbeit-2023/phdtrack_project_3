from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score
from imblearn.under_sampling import RandomUnderSampler

from feature_engineering.pipelines.univariate_feature_selection import __compute_distance_f_test_p_val
from feature_engineering.params.params import ProgramParams

import pandas as pd

def ml_random_forest_pipeline(params: ProgramParams, samples: pd.DataFrame, labels: pd.Series) -> None:
    """
    Pipeline for RandomForest with undersampling.
    """
    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(samples, labels, test_size=0.2, random_state=42)

    # Perform undersampling on the majority class
    rus = RandomUnderSampler(random_state=42)
    X_res, y_res = rus.fit_resample(X_train, y_train)

    # Train a RandomForestClassifier
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_res, y_res)

    # Make predictions on the test set
    y_pred = clf.predict(X_test)

    # Compute metrics
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    # Log the results
    params.COMMON_LOGGER.info(f'Precision: {precision}, Recall: {recall}, F1-score: {f1}')
