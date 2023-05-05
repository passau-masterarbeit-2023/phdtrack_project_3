
from feature_engineering.data_loading.data_loading import load_samples_and_labels_from_csv
from tests.tests import init_test


def test_load_samples_and_labels_from_csv():
    testParams = init_test()

    load_samples_and_labels_from_csv(
        testParams.TEST_CSV_TRAINING_1
    )
