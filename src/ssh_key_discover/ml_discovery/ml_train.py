
from .ml_data_manips import *
from .ml_utils import *
from ..mem_graph.graph_structures import *
from ..params import ProgramParams
from ..mem_graph.mem_utils import *

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC


def train_rfc(
        params: ProgramParams,
        model_name: str,
        samples: list[list[int]], 
        labels: list[int]
    ):
    """
    Train a random forest classifier.
    """
    # initialize the classifier[:10]
    clf = RandomForestClassifier(random_state=0, n_jobs=params.MAX_ML_WORKERS)

    # fit the classifier to the training data, use multi-threading
    print("Fitting the rfc classifier...")
    with time_measure('fit_rfc_classifier'):
        clf.fit(samples, labels)

    # save the model
    save_model(params, clf, model_name)

    return clf

def train_high_recall_classifier(
    params: ProgramParams,
    model_name: str,
    samples: list[list[int]], 
    labels: list[int]
):
    # set the parameter grid
    param_grid = {
        'C': [0.1, 1, 10], 
        'kernel': ['rbf'],
        'class_weight': [{0: 1, 1: 100}]
    }

    # initialize the classifier
    svc = SVC()

    # initialize the grid search #TODO: RandomizedSearchCV
    grid_search = GridSearchCV(svc, param_grid, cv=5, scoring='recall', n_jobs=params.MAX_ML_WORKERS)

    # fit the grid search to the data
    print("Fitting the grid search classifier...")
    with time_measure('fit_grid_search_classifier'):
        grid_search.fit(samples, labels)

    # print the best parameters
    print("Best parameters: ", grid_search.best_params_)

    #get the best model
    custom_clf = grid_search.best_estimator_

    # save the model
    save_model(params, custom_clf, model_name)