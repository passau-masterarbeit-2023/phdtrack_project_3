from .cli import CLIArguments
from .ml_discovery.ml_structures import ModelType, BalancingType
from .utils.utils import str2bool, str2enum

from dataclasses import dataclass
import os


@dataclass
class ProgramParams:
    """
    Wrapper class for program parameters.
    """
    cli_args: CLIArguments


    DEBUG: bool = False

    XXD_LINE_BLOCK_BYTE_SIZE = 16
    BLOCK_BYTE_SIZE = 8 # 64-bit, ex: C0 03 7B 09 2A 56 00 00
    PTR_ENDIANNESS = "little"

    # manual
    TEST_JSON_TEST_FILE_PATH = os.environ['HOME'] + "/Documents/repo_git/phdtrack_project_3/data/302-1644391327.json"
    TEST_HEAP_DUMP_RAW_FILE_PATH = os.environ['HOME'] + "/Documents/data/phdtrack/Training/scp/V_7_8_P1/16/30774-1644391327-heap.raw"
    TEST_DATA_DIR = os.environ['HOME'] + "/Documents/repo_git/phdtrack_project_3/data/graphs"
    #TEST_GRAPH_DATA_FILENAME = "graph_302-1644391327.gv"
    TEST_GRAPH_DATA_FILENAME = "467-1644391327-heap.gv"

    # ML 
    BASE_EMBEDDING_DEPTH = 5
    TRAINING_DATA_DIR_PATH = os.environ['HOME'] + "/Documents/data/phdtrack/Training/scp/V_7_8_P1/16"
    TESTING_DATA_DIR_PATH = os.environ['HOME'] + "/Documents/data/phdtrack/Validation/scp/V_7_8_P1/16"
    MODELS_DIR_PATH = os.environ['HOME'] + "/Documents/repo_git/phdtrack_project_3/models"
    SAMPLES_AND_LABELS_DATA_DIR_PATH = os.environ['HOME'] + "/Documents/repo_git/phdtrack_project_3/data/samples_and_labels"
    MAX_SAMPLES_AND_TESTINGS_WORKERS = 14
    MAX_ML_WORKERS = 2
    MODEL_TYPE: ModelType = ModelType.RFC
    BALANCING_TYPE: BalancingType = BalancingType.NONE

    def __init__(self, debug=False, **kwargs):
        self.DEBUG = debug

        self.__load_program_argv()
        self.__consume_program_argv()
        self.__check_all_paths()
        

    def __check_all_paths(self):
        """
        Check if all paths are valid.
        """
        if (
            self.__check_path_exists(self.TEST_JSON_TEST_FILE_PATH) and
            self.__check_path_exists(self.TEST_HEAP_DUMP_RAW_FILE_PATH) and
            self.__check_path_exists(self.TEST_DATA_DIR) and
            self.__check_path_exists(self.TRAINING_DATA_DIR_PATH) and
            self.__check_path_exists(self.MODELS_DIR_PATH)
        ):
            print("Program paths are OK.")
        else:
            print("Program paths are NOT OK.")
            exit(1)
    
    
    def __check_path_exists(self, path: str):
        """
        Check if the path exists. Return True if it exists, False otherwise.
        """
        if not os.path.exists(path):
            print('WARNING: Path does not exist: %s' % path)
            return False
        return True

    def __load_program_argv(self):
        """
        Load given program arguments.
        """
        self.cli_args: CLIArguments = CLIArguments()
    
    def __consume_program_argv(self):
        """
        Consume given program arguments.
        """
        if self.cli_args.args.model_type is not None:
            self.MODEL_TYPE = str2enum(
                self.cli_args.args.model_type, ModelType
            )
        if self.cli_args.args.balancing_type is not None:
            self.BALANCING_TYPE = str2enum(
                self.cli_args.args.balancing_type, BalancingType
            )
        if self.cli_args.args.training_dir_path is not None:
            self.TRAINING_DATA_DIR_PATH = self.cli_args.args.training_dir_path
        if self.cli_args.args.testing_dir_path is not None:
            self.TESTING_DATA_DIR_PATH = self.cli_args.args.testing_dir_path
        if self.cli_args.args.debug is not None:
            self.DEBUG = str2bool(self.cli_args.args.debug)
        if self.cli_args.args.max_ml_workers is not None:
            self.MAX_ML_WORKERS = int(self.cli_args.args.max_ml_workers)

PARAMS = ProgramParams()