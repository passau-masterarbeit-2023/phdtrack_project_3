from typing import Generator, Tuple, Union
from pandas import DataFrame, Series

# Define the type alias
DataGenerator = Generator[Tuple[DataFrame, Series], None, None]
DataTuple = Tuple[DataFrame, Series]

SamplesAndLabelsType = Union[DataTuple, DataGenerator]

def is_datatuple(obj) -> bool:
    return isinstance(obj, tuple) and len(obj) == 2 and isinstance(obj[0], DataFrame) and isinstance(obj[1], Series)

def is_datagenerator(obj) -> bool:
    return isinstance(obj, Generator)
