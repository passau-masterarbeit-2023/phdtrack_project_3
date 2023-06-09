
def __handle_data_origin_respecting_generator(
    data_origins: set[DataOriginEnum],
    origin_to_samples_and_labels: dict[DataOriginEnum, SamplesAndLabels]
) -> SamplesAndLabels:
    """
    Helper function for handling data origins, for classifiers that potentially use data generators.
    """

    # beware interperter on "yield from". Need to take it to its own function to avoid skipping control flow
    def concat_generators(
            data_origins: set[DataOriginEnum],
        origin_to_samples_and_labels: dict[DataOriginEnum, SamplesAndLabelsUnion]
    ):
        for data_origin in data_origins:
            # NOTE: yield from allows to yield from a generator from within a generator
            # ameno: http://simeonvisser.com/posts/python-3-using-yield-from-in-generators-part-1.html
            yield from origin_to_samples_and_labels[data_origin]


    vals = handle_data_origin(data_origins, origin_to_samples_and_labels)
    return vals
        