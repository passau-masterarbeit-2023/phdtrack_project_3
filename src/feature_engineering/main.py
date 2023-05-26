from feature_engineering.data_loading.data_loading import load
from feature_engineering.data_loading.data_cleaning import clean
from feature_engineering.params.pipeline_params import print_pipeline_names
from feature_engineering.utils.utils import time_measure
from feature_engineering.pipelines.pipelines import PIPELINE_NAME_TO_FUNCTION, check_pipelines_params, print_all_possible_pipeline_names
from feature_engineering.params.params import ProgramParams

import pandas as pd

# run: python src/feature_engineering/main.py
def main():
    print("🚀 Running program...")

    params = ProgramParams()

    # consume program argv pipelines and run them
    if params.PIPELINES is None:
        # no pipelines to run
        params.COMMON_LOGGER.warning(f"Pipelines is None (params.PIPELINES: {params.PIPELINES})")
        print_pipeline_names()
        exit(1)
    else:
        # check params.PIPELINES
        if len(params.PIPELINES) == 0:
            params.COMMON_LOGGER.warning(f"No pipelines to run (params.PIPELINES: {params.PIPELINES})")
            print_pipeline_names()
            exit(1)

        # load & clean data
        samples_and_labels = load(
            params, 
            params.CSV_DATA_SAMPLES_AND_LABELS_DIR_PATH,
            params.DATA_ORIGINS
        )
        
        for pipeline_name in params.PIPELINES:
            params.COMMON_LOGGER.info(f"Running pipeline: {pipeline_name}")
            pipeline_function: function[ProgramParams, pd.DataFrame, pd.Series] = PIPELINE_NAME_TO_FUNCTION[pipeline_name]
            with time_measure(f'pipeline ({pipeline_name})', params.RESULTS_LOGGER):
                pipeline_function(params, samples_and_labels)
                
        




if __name__ == "__main__":
    main()

