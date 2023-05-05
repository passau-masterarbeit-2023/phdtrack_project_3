"""
File used for internal testing variables and functions.
"""

from feature_engineering.params import ProgramParams

class TestParams:
    params: ProgramParams

    def __init__(self) -> None:
        self.params = ProgramParams()

        self.TEST_CSV_DATA_SAMPLES_AND_LABELS_DIR_PATH = self.params.REPO_BASE_DIR + "data/test/samples_and_labels/"

        self.TEST_CSV_TRAINING_1 = self.TEST_CSV_DATA_SAMPLES_AND_LABELS_DIR_PATH + "Training__chunck_idx-0_samples.csv"
        self.TEST_CSV_VALIDATION = self.TEST_CSV_DATA_SAMPLES_AND_LABELS_DIR_PATH + "Validation__chunck_idx-0_samples.csv"

def init_test():
    """
    Initialize the test.
    """

    return TestParams()
    

    

