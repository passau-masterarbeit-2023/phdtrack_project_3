from value_node_ml.params.pipeline_params import PipelineNames
from value_node_ml.pipelines.ml.ml_sgd import ml_sgd_pipeline
from value_node_ml.pipelines.feature_engineering.univariate_feature_selection import univariate_feature_selection_pipeline
from value_node_ml.pipelines.ml.ml_logistic_regression import ml_logistic_regression_pipeline
from value_node_ml.pipelines.check import check
from value_node_ml.pipelines.ml.ml_random_forest import ml_random_forest_pipeline

PIPELINE_NAME_TO_FUNCTION = {
    PipelineNames.CHECK : check,
    PipelineNames.UNIVARIATE_FS : univariate_feature_selection_pipeline,
    PipelineNames.ML_LOGISTIC_REG : ml_logistic_regression_pipeline,
    PipelineNames.ML_RANDOM_FOREST : ml_random_forest_pipeline,
    PipelineNames.ML_SGD : ml_sgd_pipeline,
}

