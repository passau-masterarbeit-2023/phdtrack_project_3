from enum import Enum

from commons.utils.enum_utils import print_enum_values, convert_str_arg_to_enum_member


class PipelineNames(Enum):
    """
    Pipeline names.
    """
    CHECK = "check"

    # ML
    ML_LOGISTIC_REG = "ml_logistic_reg"
    ML_RANDOM_FOREST = "ml_random_forest"
    ML_SGD = "ml_sgd"

    # feature engineering
    FE_UNIVARIATE = "fe_univariate"
    FE_CORR_PEARSON = "fe_corr_pearson" 
    FE_CORR_KENDALL = "fe_corr_kendall"
    FE_CORR_SPEARMAN = "fe_corr_spearman"

def is_feature_engineering_pipeline(pipeline_name: PipelineNames):
    """
    Return True if the pipeline is a feature engineering pipeline.
    """
    return pipeline_name in [
        PipelineNames.FE_UNIVARIATE,
        PipelineNames.FE_CORR_PEARSON,
        PipelineNames.FE_CORR_KENDALL,
        PipelineNames.FE_CORR_SPEARMAN,
    ]

def print_pipeline_names():
    """
    Print the possible values of the PipelineNames.
    """
    print_enum_values(PipelineNames)


def convert_str_arg_to_pipeline_name(arg: str):
    """
    Convert a string argument to a PipelineNames.
    """
    return convert_str_arg_to_enum_member(arg, PipelineNames)


