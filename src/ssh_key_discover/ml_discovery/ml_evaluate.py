from .ml_utils import time_measure
from ..params import ProgramParams

from typing import Any
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import confusion_matrix, roc_curve, auc


    
def evaluate(
        params: ProgramParams,
        clf: Any, 
        test_samples: list[list[int]], 
        test_labels: list[int]
    ):
    """
    Evaluate the model.
    """
    # evaluate the model
    with time_measure('evaluate_model_score', params.RESULTS_LOGGER):
        
        # make predictions on the test data
        y_pred = clf.predict(test_samples)
        params.RESULTS_LOGGER.info(
            "Sample of predicted labels: %s \n versus actual labels: %s", y_pred[:20], test_labels[:20]
        )

        # calculate the accuracy of the model
        accuracy = accuracy_score(test_labels, y_pred)
        params.RESULTS_LOGGER.info("Accuracy: {:.2f}%".format(accuracy * 100))

        # print the classification report
        params.RESULTS_LOGGER.info(classification_report(test_labels, y_pred))


        # calculate the confusion matrix
        cm = confusion_matrix(test_labels, y_pred)
        params.RESULTS_LOGGER.info("Confusion Matrix: ")
        params.RESULTS_LOGGER.info("True Positives: %d", cm[1, 1])
        params.RESULTS_LOGGER.info("True Negatives: %d", cm[0, 0])
        params.RESULTS_LOGGER.info("False Positives: %d", cm[0, 1])
        params.RESULTS_LOGGER.info("False Negatives: %d", cm[1, 0])

        # calculate the false positive rate and true positive rate
        fpr, tpr, thresholds = roc_curve(test_labels, y_pred)

        # calculate the area under the ROC curve
        roc_auc = auc(fpr, tpr)
        params.RESULTS_LOGGER.info("AUC: {:.2f}".format(roc_auc))

        # plot the ROC curve
        import matplotlib.pyplot as plt
        plt.plot(fpr, tpr, label='ROC curve (area = {:.2f})'.format(roc_auc))
        plt.plot([0, 1], [0, 1], 'k--')  # random predictions curve
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.0])
        plt.xlabel('False Positive Rate or (1 - Specifity)')
        plt.ylabel('True Positive Rate or (Sensitivity)')
        plt.title('Receiver Operating Characteristic')
        plt.legend(loc="lower right")
        plt.show()