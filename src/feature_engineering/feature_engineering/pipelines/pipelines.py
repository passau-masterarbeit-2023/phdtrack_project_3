from feature_engineering.params import ProgramParams
from feature_engineering.pipelines.univariate_feature_selection import univariate_feature_selection_pipeline

PIPELINE_NAME_TO_FUNCTION = {
    "univariate_fs": univariate_feature_selection_pipeline,
}

def print_all_possible_pipeline_names(params: ProgramParams) -> None:
    params.COMMON_LOGGER.info("All possible pipeline names:")
    for pipeline_name in PIPELINE_NAME_TO_FUNCTION:
        params.COMMON_LOGGER.info(f"    * {pipeline_name}")