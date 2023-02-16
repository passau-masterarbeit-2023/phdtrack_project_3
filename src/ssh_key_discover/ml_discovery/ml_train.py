from sklearn.ensemble import RandomForestClassifier

from .ml_data_manips import *
from .ml_utils import *
from ..mem_graph.graph_structures import *
from ..params import ProgramParams
from ..mem_graph.mem_utils import *


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
    clf = RandomForestClassifier(random_state=0, n_jobs=-1)

    # fit the classifier to the training data, use multi-threading
    print("Fitting the classifier...")
    with time_measure('fit_classifier'):
        clf.fit(samples, labels)

    # save the model
    save_model(params, clf, model_name)

    return clf