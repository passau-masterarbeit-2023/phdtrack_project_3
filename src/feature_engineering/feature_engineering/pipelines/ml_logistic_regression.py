from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, precision_score, recall_score

from feature_engineering.pipelines.univariate_feature_selection import __compute_distance_f_test_p_val
from feature_engineering.params.params import ProgramParams

import pandas as pd

def ml_logistic_regression_pipeline(params: ProgramParams, samples: pd.DataFrame, labels: pd.Series) -> None:
    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(samples, labels, test_size=0.2, random_state=42)

    # Feature selection
    selector = SelectKBest(f_classif, k=10)
    X_train_transformed = selector.fit_transform(X_train, y_train)
    column_names = samples.columns[selector.get_support()].tolist()
    print("column_names:", column_names, "type:", type(column_names))

    f_values, p_values = selector.score_func(samples, labels)
    column_names2 = samples.columns.tolist()

    print("column_names2:", column_names2, "type:", type(column_names2))


    # Train classifier
    clf = LogisticRegression()
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
