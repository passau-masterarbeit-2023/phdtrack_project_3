# direct raw access to params
import sys
import argparse

# wrapped program flags
class CLIArguments:
    args: argparse.Namespace

    def __init__(self) -> None:
        self.__log_raw_argv()
        self.__parse_argv()
    
    def __log_raw_argv(self) -> None:
        print("Passed program params:")
        for i in range(len(sys.argv)):
            print("param[{0}]: {1}".format(
                i, sys.argv[i]
            ))
    
    def __parse_argv(self) -> None:
        """
        python src/main.py [ARGUMENTS ...]

        Parse program arguments.
            -m model type (ml_structures.ModelType: RFC, GRID_SEARCH_CV)
            -b balancing type (ml_structures.BalancingType: NONE, OVER, UNDER)
            -t training dir path, path to the heap dump raw files
            -e testing dir path, path to the heap dump raw files
            -w max ml workers (threads for ML threads pool, -1 for illimited)
            -d debug
            -v vectorizing depth (influence the size of the feature vector)
            -h help
        
        usage example:
            python3 main.py -m GRID_SEARCH_CV -b OVER -t /home/onyr/Documents/code/phdtrack/phdtrack_data/Training/Training/scp/V_7_8_P1/16 -e /home/onyr/Documents/code/phdtrack/phdtrack_data/Validation/Validation/scp/V_7_8_P1/16 -d False -v 2
        """
        parser = argparse.ArgumentParser(description='Program [ARGUMENTS]')
        parser.add_argument(
            '-m',
            '--model_type', 
            type=str, 
            default=None,
            help="model type (ml_structures.ModelType: RFC, GRID_SEARCH_CV)"
        )
        parser.add_argument(
            '-b',
            '--balancing_type', 
            type=str, 
            default=None,
            help="balancing type (ml_structures.BalancingType: NONE, OVER, UNDER)"
        )
        parser.add_argument(
            '-t',
            '--training_dir_path', 
            type=str, 
            default=None,
            help="training dir path, path to the heap dump raw files"
        )
        parser.add_argument(
            '-e',
            '--testing_dir_path', 
            type=str, 
            default=None,
            help="testing dir path, path to the heap dump raw files"
        )
        parser.add_argument(
            '-d',
            '--debug', 
            type=bool, 
            default=None,
            help="debug, True or False"
        )
        parser.add_argument(
            '-v',
            '--vectorizing_depth', 
            type=int, 
            default=None,
            help="vectorizing depth (influence the size of the feature vector)"
        )
        parser.add_argument(
            '-w',
            '--max_ml_workers', 
            type=int, 
            default=None,
            help="max ml workers (threads for ML threads pool, -1 for illimited)"
        )

        # save parsed arguments
        self.args = parser.parse_args()