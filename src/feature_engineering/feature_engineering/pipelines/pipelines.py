from feature_engineering.pipelines.ml_sgd import ml_sgd_pipeline
from feature_engineering.params.params import ProgramParams
from feature_engineering.pipelines.univariate_feature_selection import univariate_feature_selection_pipeline
from feature_engineering.pipelines.ml_logistic_regression import ml_logistic_regression_pipeline
from feature_engineering.pipelines.check import check
from feature_engineering.pipelines.ml_random_forest import ml_random_forest_pipeline

PIPELINE_NAME_TO_FUNCTION = {
    "check": check,
    "univariate_fs": univariate_feature_selection_pipeline,
    "ml_logistic_reg": ml_logistic_regression_pipeline,
    "ml_random_forest": ml_random_forest_pipeline,
    "ml_sgd": ml_sgd_pipeline,
}

def print_all_possible_pipeline_names(params: ProgramParams) -> None:
    params.COMMON_LOGGER.info("All possible pipeline names:")
    for pipeline_name in PIPELINE_NAME_TO_FUNCTION:
        params.COMMON_LOGGER.info(f"    * {pipeline_name}")

def check_pipelines_params(params: ProgramParams) -> None:
    for pipeline_name in params.PIPELINES:
        if pipeline_name not in PIPELINE_NAME_TO_FUNCTION:
            # pipeline does not exist
            params.COMMON_LOGGER.error(f"Pipeline {pipeline_name} does not exist.")
            print_all_possible_pipeline_names(params)
            # log error and exit
            params.COMMON_LOGGER.error(f"Pipeline {pipeline_name} does not exist.")
            exit(1)