from .ml_utils import time_measure
from ..params import ProgramParams

from typing import Any


class MLEvaluator:
    params: ProgramParams

    def __init__(self, params: ProgramParams):
        self.params = params
    
    def evaluate(self, clf: Any, samples, labels):
        """
        Evaluate the model.
        """
        # evaluate the model
        print("Evaluating the model...")
        with time_measure('evaluate_model'):
            clf.score(samples, labels)