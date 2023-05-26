
import pandas as pd
from feature_engineering.data_loading.data_loading import consume_data_generator
from feature_engineering.data_loading.data_types import SamplesAndLabelsGenerator, SamplesAndLabels, SamplesAndLabelsUnion, is_datagenerator, is_datatuple
from feature_engineering.params.data_origin import DataOriginEnum


def handle_data_origin_consume_generator(
    data_origins: set[DataOriginEnum],
    origin_to_samples_and_labels: dict[DataOriginEnum, SamplesAndLabelsUnion]
):
    """
    Helper function for handling data origins, for classifiers that do not use data generators.
    """
    __samples: list[pd.DataFrame] = []
    __labels: list[pd.Series] = []
    for origin in data_origins:
        samples_and_labels = origin_to_samples_and_labels[origin]

        if is_datatuple(samples_and_labels):
            samples, labels = samples_and_labels
            __labels += [labels]
            __samples += [samples]
        elif is_datagenerator(samples_and_labels):
            # consume the data generator
            samples, labels = consume_data_generator(samples_and_labels)
            __labels += [labels]
            __samples += [samples]
        else:
            raise TypeError(f"Invalid type for samples_and_labels: {type(samples_and_labels)}")
    samples_and_labels = (pd.concat(__samples), pd.concat(__labels))
    return samples_and_labels


def handle_data_origin_respecting_generator(
    data_origins: set[DataOriginEnum],
    origin_to_samples_and_labels: dict[DataOriginEnum, SamplesAndLabelsUnion]
) -> SamplesAndLabelsUnion:
    """
    Helper function for handling data origins, for classifiers that potentially use data generators.
    """
    print("28237373737")
    first_samples_and_labels = next(iter(origin_to_samples_and_labels.values())) # get first value, without iterating
    if is_datagenerator(first_samples_and_labels):
        print("is_datagenerator")
        for data_origin in data_origins:
            # NOTE: yield from allows to yield from a generator from within a generator
            # ameno: http://simeonvisser.com/posts/python-3-using-yield-from-in-generators-part-1.html
            yield from origin_to_samples_and_labels[data_origin] 
    elif is_datatuple(first_samples_and_labels):
        vals = handle_data_origin_consume_generator(data_origins, origin_to_samples_and_labels)
        print("vals", vals)
        print("vals type", type(vals))
        return vals
    else:
        raise TypeError(f"Invalid type for samples_and_labels: {type(first_samples_and_labels)}")
            

