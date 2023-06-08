from datetime import datetime
import json
import contextlib
import time
import logging

from common.results.base_result_manager import BaseResultsManager
from common.results.base_result_writer import BaseResultWriter

# utils constants
DATETIME_FORMAT = "%Y_%m_%d_%H_%M_%S_%f"


def str2bool(string: str) -> bool:
    return json.loads(string.lower())


def str2enum(string: str, enum_type: type):
    return enum_type[string.upper()]


@contextlib.contextmanager
def time_measure_result(
    message: str, 
    logger : logging.Logger = None,
    result_saver: BaseResultWriter | BaseResultsManager = None, 
    result_column: str = None, 
):
    """
    Measure the time elapsed since the begining of the context.
    """
    if logger is not None:
        logger.info("timer for " + message + " started")
    else:
        print("timer for " + message + " started")

    start = datetime.now()
    yield
    elapsed = datetime.now() - start
    # duration in seconds with 6 decimals
    duration_str = f"{elapsed.total_seconds():.9f}"

    message = "Time elapsed since the begining of {0}: {1} s".format(message, duration_str)
    
    if logger is not None:
        logger.info(message)
    else:
        print(message)
    
    if result_saver is not None and result_column is not None:
        if type(result_saver) == BaseResultsManager:
            result_saver.set_result_forall(result_column, duration_str)
        elif type(result_saver) == BaseResultWriter:
            result_saver.set_result(result_column, duration_str)
        else:
            raise ValueError(f"Unknown result saver type: {type(result_saver)}")
    

def datetime2str(datetime: datetime):
    """
    Return a string representation of the given datetime.
    NB: The %f is the microseconds.
    """
    return datetime.strftime(DATETIME_FORMAT)



