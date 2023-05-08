from feature_engineering.params.params import ProgramParams
from feature_engineering.pipelines.univariate_feature_selection import univariate_feature_selection_pipeline
from feature_engineering.pipelines.check import check

PIPELINE_NAME_TO_FUNCTION = {
    "check": check,
    "univariate_fs": univariate_feature_selection_pipeline,
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
            raise ValueError(f"Pipeline {pipeline_name} does not exist.")