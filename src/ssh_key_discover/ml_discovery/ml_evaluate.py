from .ml_utils import time_measure
from ..params import ProgramParams

from typing import Any
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import confusion_matrix, roc_curve, auc


    
def evaluate(
        clf: Any, 
        test_samples: list[list[int]], 
        test_labels: list[int]
    ):
    """
    Evaluate the model.
    """
    # evaluate the model
    print("Evaluating the model...")
    with time_measure('evaluate_model_score'):
        
        # make predictions on the test data
        y_pred = clf.predict(test_samples)
        print(
            "Sample of predicted labels:", y_pred[:20], 
            "versus actual labels:", test_labels[:20], sep="\n"
        )

        # calculate the accuracy of the model
        accuracy = accuracy_score(test_labels, y_pred)
        print("Accuracy: {:.2f}%".format(accuracy * 100))

        # print the classification report
        print(classification_report(test_labels, y_pred))


        # calculate the confusion matrix
        cm = confusion_matrix(test_labels, y_pred)
        print("Confusion Matrix: \n", cm)
        print("True Positives: ", cm[1, 1])
        print("True Negatives: ", cm[0, 0])
        print("False Positives: ", cm[0, 1])
        print("False Negatives: ", cm[1, 0])

        # calculate the false positive rate and true positive rate
        fpr, tpr, thresholds = roc_curve(test_labels, y_pred)

        # calculate the area under the ROC curve
        roc_auc = auc(fpr, tpr)
        print("AUC: {:.2f}".format(roc_auc))

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