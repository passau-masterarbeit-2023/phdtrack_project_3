from .cli import CLIArguments
from .ml_discovery.ml_structures import ModelType, BalancingType
from .utils.utils import str2bool, str2enum

from dataclasses import dataclass
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime


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

    # logger
    COMMON_LOGGER_DIR_PATH = os.environ['HOME'] + "/Documents/repo_git/phdtrack_project_3/data/logs/common_log"
    RESULTS_LOGGER_DIR_PATH = os.environ['HOME'] + "/Documents/repo_git/phdtrack_project_3/data/logs/results_log"
    COMMON_LOGGER = logging.getLogger("common_logger")
    RESULTS_LOGGER = logging.getLogger("results_logger")

    def __init__(self, **kwargs):
        self.__load_program_argv()
        self.__consume_program_argv()
        self.__check_all_paths()

        self.__construct_log()
        self.__log_program_params()
        

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

    def __construct_log(self):
        """
        construct logger. Must be call after __load_program_argv()
        """
        # common formater
        common_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # ----------------- common logger -----------------
        # create common logger
        self.COMMON_LOGGER.setLevel(logging.DEBUG)

        # add RotatingFileHandler to common logger
        common_log_file_path = self.COMMON_LOGGER_DIR_PATH + "/common_log.log"
        common_log_file_handler = RotatingFileHandler(
            common_log_file_path, maxBytes=50000000, backupCount=5
        )
        logging_level = logging.DEBUG if self.DEBUG else logging.INFO
        common_log_file_handler.setLevel(logging_level)
        common_log_file_handler.setFormatter(common_formatter)
        self.COMMON_LOGGER.addHandler(common_log_file_handler)

        # add console handler to common logger
        common_log_console_handler = logging.StreamHandler(stream=sys.stdout)
        common_log_console_handler.setLevel(logging.ERROR)
        common_log_console_handler.setFormatter(common_formatter)
        self.COMMON_LOGGER.addHandler(common_log_console_handler)

        # ----------------- results logger -----------------
        # create results logger
        self.RESULTS_LOGGER.setLevel(logging.DEBUG)

        # Result logger using file handler
        results_log_file_path = self.RESULTS_LOGGER_DIR_PATH + "/" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "_results.log"
        results_log_file_handler = logging.FileHandler(results_log_file_path)
        results_log_file_handler.setLevel(logging.DEBUG)
        results_log_file_handler.setFormatter(common_formatter)
        self.RESULTS_LOGGER.addHandler(results_log_file_handler)

        # Result logger using console handler
        results_log_console_handler = logging.StreamHandler(stream=sys.stdout)
        results_log_console_handler.setLevel(logging.DEBUG)
        results_log_console_handler.setFormatter(common_formatter)
        self.RESULTS_LOGGER.addHandler(results_log_console_handler)
    
    def __log_program_params(self):
        """
        Log given program arguments.
        """
        self.RESULTS_LOGGER.info("Program params:")
        self.RESULTS_LOGGER.info("model_type: %s" % self.MODEL_TYPE)
        self.RESULTS_LOGGER.info("balancing_type: %s" % self.BALANCING_TYPE)
        self.RESULTS_LOGGER.info("training_dir_path: %s" % self.TRAINING_DATA_DIR_PATH)
        self.RESULTS_LOGGER.info("testing_dir_path: %s" % self.TESTING_DATA_DIR_PATH)
        self.RESULTS_LOGGER.info("debug: %s" % self.DEBUG)
        self.RESULTS_LOGGER.info("max_ml_workers: %s" % self.MAX_ML_WORKERS)
        self.RESULTS_LOGGER.info("Base embedding depth: %s" % self.BASE_EMBEDDING_DEPTH)