from feature_engineering.results.results_manager import ResultsManager
from .data_origin import DataOriginEnum, convert_str_arg_to_data_origin, print_data_origin_enum
from ..cli import CLIArguments
from ..utils.utils import DATETIME_FORMAT, datetime2str
from feature_engineering.params.pipeline_params import PipelineNames, convert_str_arg_to_pipeline_name, print_pipeline_names

from dataclasses import dataclass
import dotenv
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
    results_manager: ResultsManager

    # default values
    DEBUG: bool = False
    MAX_ML_WORKERS = 10
    PIPELINES: list[PipelineNames] | None = None
    DATA_ORIGINS_TRAINING: set[DataOriginEnum] | None = None
    DATA_ORIGINS_TESTING: set[DataOriginEnum] | None = None
    BATCH: bool = False

    # base directories
    REPO_BASE_DIR = os.environ['HOME'] + "/code/phdtrack/phdtrack_project_3/"
    DATA_BASE_DIR = os.environ['HOME'] + "/code/phdtrack/phdtrack_data/"
    PROJECT_BASE_DIR = REPO_BASE_DIR + "src/features_engineering/"

    # data
    CSV_DATA_SAMPLES_AND_LABELS_DIR_PATH = REPO_BASE_DIR + "src/mem_to_graph/data/samples_and_labels/"

    # results
    CSV_CLASSIFICATION_RESULTS_PATH = REPO_BASE_DIR + "results/classification_results.csv"

    # logger
    COMMON_LOGGER_DIR_PATH = REPO_BASE_DIR + "data/logs/common_log/"
    RESULTS_LOGGER_DIR_PATH = REPO_BASE_DIR + "data/logs/results_log/"
    COMMON_LOGGER = logging.getLogger("common_logger")
    RESULTS_LOGGER = logging.getLogger("results_logger")


    USE_IMPORTANT_LOG_FILE = True

    def __init__(self, load_program_argv : bool = True, debug : bool = False, generate_important_log_file = True, **kwargs):
        """
        Program parameters. If load_program_argv is True, the program parameters are loaded from the command line arguments.
        Otherwise, the program parameters are loaded from the default values.
        if generate_important_log_file is True, the program will generate an important log file with the current date and time.
        otherwise, the program will use the default log file.

        debug and generate_important_log_file parameter is used only if load_program_argv is True.
        """
        if load_program_argv:
            self.__parse_program_argv()
        else:
            self.DEBUG = debug
            self.USE_IMPORTANT_LOG_FILE = generate_important_log_file

        self.__load_env()
        self.__check_all_paths()

        self.__construct_log()
        self.__log_program_params()

        # keep results
        self.results_manager = ResultsManager(
            self.CSV_CLASSIFICATION_RESULTS_PATH
        )
        # self.results_manager.set_result_forall(
        #     "balancing_type", ...
        # )  
        # self.results_manager.set_result_forall(
        #     "training_dataset_origin", ...
        # )
        # self.results_manager.set_result_forall(
        #     "testing_dataset_origin", ...
        # )
    
    @classmethod
    def __load_env(self):
        """
        Load environment variables from .env file.
        Overwrite default values with values from .env file if they are defined there.
        """
        dotenv.load_dotenv(dotenv_path=self.PROJECT_BASE_DIR + ".env")

        # Overwrite default values with values from .env file if they are defined there
        # NOTE: cls.__annotations__ is a dictionary where the keys are the names of 
        #   the class variables and the values are their types
        for variable in self.__annotations__.keys():
            env_value = os.getenv(variable)
            if env_value is not None:
                # Convert to the appropriate type
                if self.__annotations__[variable] == bool:
                    env_value = env_value.lower() == 'true'
                elif self.__annotations__[variable] == int:
                    env_value = int(env_value)
                elif self.__annotations__[variable] == list:
                    env_value = env_value.split(',')
                setattr(self, variable, env_value)




    def __is_running_under_pytest(self):
        """
        Check whether the code is running under pytest.
        """
        return 'pytest' in sys.modules

    def __check_all_paths(self):
        """
        Check if all paths are valid.
        """
        if (
            self.__check_path_exists(self.COMMON_LOGGER_DIR_PATH) and
            self.__check_path_exists(self.RESULTS_LOGGER_DIR_PATH) 
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
    
    def __parse_program_argv(self):
        """
        Parse program arguments.
        WARN: Do NOT parse program argv if running under pytest.
        """
        if not self.__is_running_under_pytest():
            self.__load_program_argv()
            self.__consume_program_argv()
    
    def __load_program_argv(self):
        """
        Load given program arguments.
        """
        self.cli_args: CLIArguments = CLIArguments()
    
    def __consume_program_argv(self):
        """
        Consume given program arguments.
        """
        if self.cli_args.args.debug is not None:
            self.DEBUG = self.cli_args.args.debug
            assert isinstance(self.DEBUG, bool)

        if self.cli_args.args.max_ml_workers is not None:
            self.MAX_ML_WORKERS = int(self.cli_args.args.max_ml_workers)
            assert isinstance(self.MAX_ML_WORKERS, int)

        if self.cli_args.args.origins_training is not None:
            try:
                self.DATA_ORIGINS_TRAINING = set(map(convert_str_arg_to_data_origin, self.cli_args.args.origins_training))
                assert isinstance(self.DATA_ORIGINS_TRAINING, set)
            except ValueError:
                print(f"ERROR: Invalid data origin training: {self.cli_args.args.origins_training}")
                exit(1)
        
        if self.cli_args.args.origins_testing is not None:
            try:
                self.DATA_ORIGINS_TESTING = set(map(convert_str_arg_to_data_origin, self.cli_args.args.origins_testing))
                assert isinstance(self.DATA_ORIGINS_TESTING, set)
            except ValueError:
                print(f"ERROR: Invalid data origin testing: {self.cli_args.args.origins_testing}")
                exit(1)
            # NOTE: please, let DATA_ORIGINS_TESTING to none, such that we can split the data in the pipeline if needed.
        
        if self.cli_args.args.pipelines is not None:
            try:
                self.PIPELINES = set(map(convert_str_arg_to_pipeline_name, self.cli_args.args.pipelines))
                assert isinstance(self.PIPELINES, set)
            except ValueError:
                    print(f"ERROR: Invalid pipeline name: {self.cli_args.args.pipelines}")
                    exit(1)
        # No if here, batch is either True or False
        self.BATCH = self.cli_args.args.batch
        assert isinstance(self.BATCH, bool)

    def __construct_log(self):
        """
        construct logger. Must be call after __load_program_argv()
        """
        # common formater
        common_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt=DATETIME_FORMAT.replace("_%f", "")
        )

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
        common_log_console_handler.setLevel(logging.INFO)
        common_log_console_handler.setFormatter(common_formatter)
        self.COMMON_LOGGER.addHandler(common_log_console_handler)

        # ----------------- results logger -----------------
        # create results logger
        self.RESULTS_LOGGER.setLevel(logging.DEBUG)

        # Result logger using file handler
        if self.USE_IMPORTANT_LOG_FILE:
            results_log_file_path = self.RESULTS_LOGGER_DIR_PATH + "/" + datetime2str(datetime.now()) + "_results.log"
        else:
            results_log_file_path = common_log_file_path
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
        self.RESULTS_LOGGER.info("Program params:   [see below]")
        # complete list of program params below
        self.RESULTS_LOGGER.info("\tdebug: %s" % self.DEBUG)
        self.RESULTS_LOGGER.info("\tmax_ml_workers: %s" % self.MAX_ML_WORKERS)