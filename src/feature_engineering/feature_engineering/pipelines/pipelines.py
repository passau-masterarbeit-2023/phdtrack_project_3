from feature_engineering.params.pipeline_params import PipelineNames
from feature_engineering.pipelines.ml_sgd import ml_sgd_pipeline
from feature_engineering.params.params import ProgramParams
from feature_engineering.pipelines.univariate_feature_selection import univariate_feature_selection_pipeline
from feature_engineering.pipelines.ml_logistic_regression import ml_logistic_regression_pipeline
from feature_engineering.pipelines.check import check
from feature_engineering.pipelines.ml_random_forest import ml_random_forest_pipeline

PIPELINE_NAME_TO_FUNCTION = {
    PipelineNames.CHECK : check,
    PipelineNames.UNIVARIATE_FS : univariate_feature_selection_pipeline,
    PipelineNames.ML_LOGISTIC_REG : ml_logistic_regression_pipeline,
    PipelineNames.ML_RANDOM_FOREST : ml_random_forest_pipeline,
    PipelineNames.ML_SGD : ml_sgd_pipeline,
}

