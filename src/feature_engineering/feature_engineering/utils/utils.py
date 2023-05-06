import json
import contextlib
import time
import logging


def str2bool(string: str) -> bool:
    return json.loads(string.lower())


def str2enum(string: str, enum_type: type):
    return enum_type[string.upper()]


@contextlib.contextmanager
def time_measure(ident, logger : logging.Logger = None):
    """
    Measure the time elapsed since the begining of the context.
    """
    if logger is not None:
        logger.info("timer for " + ident + " started")
    else:
        print("timer for " + ident + " started")
    tstart = time.time()
    yield
    elapsed = time.time() - tstart
    message = "Time elapsed since the begining of {0}: {1} s".format(ident, elapsed)
    if logger is not None:
        logger.info(message)
    else:
        print(message)