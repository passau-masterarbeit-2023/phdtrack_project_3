from feature_engineering.feature_engineering.data_loading.data_loading import load_samples_and_labels_from_csv
from feature_engineering.params import ProgramParams


# run: python src/feature_engineering/main.py
def main():
    print("Running program...")
    print("Program finished.")

    params = ProgramParams()


    load_samples_and_labels_from_csv(
        params.DATA_SAMPLES_AND_LABELS_CSV_DIR_PATH + ""
    )




if __name__ == "__main__":
    main()

