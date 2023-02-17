import contextlib
import time

from ..params import ProgramParams
import os

@contextlib.contextmanager
def time_measure(ident):
    tstart = time.time()
    yield
    elapsed = time.time() - tstart
    print("{0}: {1} s".format(ident, elapsed))

def get_name_for_feature_and_label_save_file(
    params : ProgramParams, 
    files_dir_origin : str, 
    testing_dir_path : str
):
    """
    Get the name for feature and label save file.
    """
    filepath_components = testing_dir_path.split(os.sep)
    filepath_components = filepath_components[-4:]
    samples_and_labels_save_file_name = "samples_and_labels_{}__depth_{}_{}.pkl".format(
        files_dir_origin,
        params.BASE_EMBEDDING_DEPTH,
        "_".join(filepath_components)
    )
    return samples_and_labels_save_file_name