from feature_engineering.params.pipeline_params import PipelineNames
from feature_engineering.pipelines.ml_sgd import ml_sgd_pipeline
from feature_engineering.params.params import ProgramParams
from feature_engineering.pipelines.univariate_feature_selection import univariate_feature_selection_pipeline
from feature_engineering.pipelines.ml_logistic_regression import ml_logistic_regression_pipeline
from feature_engineering.pipelines.check import check
from feature_engineering.pipelines.ml_random_forest import ml_random_forest_pipeline

PIPELINE_NAME_TO_FUNCTION = {
    PipelineNames.CHECK.value: check,
    PipelineNames.UNIVARIATE_FS.value: univariate_feature_selection_pipeline,
    PipelineNames.ML_LOGISTIC_REG.value: ml_logistic_regression_pipeline,
    PipelineNames.ML_RANDOM_FOREST.value: ml_random_forest_pipeline,
    PipelineNames.ML_SGD.value: ml_sgd_pipeline,
}

