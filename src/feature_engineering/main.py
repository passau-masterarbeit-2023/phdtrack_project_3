from feature_engineering.data_loading.data_loading import load_samples_and_labels_from_csv
from feature_engineering.utils.utils import time_measure
from feature_engineering.pipelines.pipelines import PIPELINE_NAME_TO_FUNCTION, print_all_possible_pipeline_names
from feature_engineering.pipelines.univariate_feature_selection import univariate_feature_selection_pipeline
from feature_engineering.params import ProgramParams


# run: python src/feature_engineering/main.py
def main():
    print("Running program...")
    print("Program finished.")

    params = ProgramParams()

    # consume program argv pipelines and run them
    if params.PIPELINES is None:
        # no pipelines to run
        params.COMMON_LOGGER.warning(f"Pipelines is None (params.PIPELINES: {params.PIPELINES})")
        print_all_possible_pipeline_names(params)
    else:
        # check params.PIPELINES
        if len(params.PIPELINES) == 0:
            params.COMMON_LOGGER.warning(f"No pipelines to run (params.PIPELINES: {params.PIPELINES})")
            print_all_possible_pipeline_names(params)

        for pipeline_name in params.PIPELINES:
            if pipeline_name in PIPELINE_NAME_TO_FUNCTION:
                params.COMMON_LOGGER.info(f"Running pipeline: {pipeline_name}")
                pipeline_function = PIPELINE_NAME_TO_FUNCTION[pipeline_name]
                with time_measure(f'main pipeline launch: {pipeline_name}', params.RESULTS_LOGGER):
                    pipeline_function(params, params.CSV_DATA_SAMPLES_AND_LABELS_DIR_PATH)
            else:
                # pipeline does not exist
                params.COMMON_LOGGER.error(f"Pipeline {pipeline_name} does not exist.")
        




if __name__ == "__main__":
    main()

