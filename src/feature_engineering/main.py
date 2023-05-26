from feature_engineering.data_loading.data_loading import load
from feature_engineering.data_loading.data_types import SamplesAndLabelsUnion
from feature_engineering.params.data_origin import DataOriginEnum
from feature_engineering.params.pipeline_params import print_pipeline_names
from feature_engineering.utils.utils import time_measure
from feature_engineering.pipelines.pipelines import PIPELINE_NAME_TO_FUNCTION
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

    if len(params.PIPELINES) == 0:
        params.COMMON_LOGGER.warning(f"No pipelines to run (params.PIPELINES: {params.PIPELINES})")
        print_pipeline_names()
        exit(1)

    if params.DATA_ORIGINS_TRAINING is None or len(params.DATA_ORIGINS_TRAINING) == 0:
        params.COMMON_LOGGER.warning(f"No training data origins (params.DATA_ORIGINS_TRAINING: {params.DATA_ORIGINS_TRAINING})")
        exit(1)
    
    # check that params.DATA_ORIGINS_TRAINING and params.DATA_ORIGINS_TESTING are disjoint
    if params.DATA_ORIGINS_TESTING is not None and len(params.DATA_ORIGINS_TESTING) > 0:
        if len(params.DATA_ORIGINS_TRAINING.intersection(params.DATA_ORIGINS_TESTING)) > 0:
            params.COMMON_LOGGER.warning(f"Training and testing data origins are not disjoint (params.DATA_ORIGINS_TRAINING: {params.DATA_ORIGINS_TRAINING}, params.DATA_ORIGINS_TESTING: {params.DATA_ORIGINS_TESTING})")
            exit(1)

    # load & clean data
    origin_to_samples_and_labels: dict[DataOriginEnum, SamplesAndLabelsUnion] = {}
    
    all_origins = params.DATA_ORIGINS_TRAINING
    if params.DATA_ORIGINS_TESTING is not None:
        all_origins = all_origins.union(params.DATA_ORIGINS_TESTING)

    for data_origin in all_origins:
        print(f"Loading data from {data_origin}")
        origin_to_samples_and_labels[data_origin] = load(
            params, 
            params.CSV_DATA_SAMPLES_AND_LABELS_DIR_PATH,
            {data_origin},
        )
    
    for pipeline_name in params.PIPELINES:
        params.COMMON_LOGGER.info(f"Running pipeline: {pipeline_name}")
        pipeline_function: function[ProgramParams, pd.DataFrame, pd.Series] = PIPELINE_NAME_TO_FUNCTION[pipeline_name]
        with time_measure(f'pipeline ({pipeline_name})', params.RESULTS_LOGGER):
            pipeline_function(params, origin_to_samples_and_labels)
                
        




if __name__ == "__main__":
    main()

