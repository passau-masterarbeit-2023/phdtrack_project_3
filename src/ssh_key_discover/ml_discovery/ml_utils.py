import contextlib
import time

@contextlib.contextmanager
def time_measure(ident):
    tstart = time.time()
    yield
    elapsed = time.time() - tstart
    print("{0}: {1} s".format(ident, elapsed))