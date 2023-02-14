from dataclasses import dataclass
import os

@dataclass
class ProgramParams:
    """
    Wrapper class for program parameters.
    """
    DEBUG: bool

    XXD_LINE_BLOCK_BYTE_SIZE = 16
    POINTER_BYTE_SIZE = 8 # 64-bit, ex: C0 03 7B 09 2A 56 00 00

    TEST_JSON_TEST_FILE_PATH = os.environ['HOME'] + "/Documents/code/phdtrack/phdtrack_project_3/data/302-1644391327.json"
    TEST_HEAP_DUMP_RAW_FILE_PATH = os.environ['HOME'] + "/Documents/code/phdtrack/phdtrack_data/Training/Training/scp/V_7_8_P1/16/362-1644391327-heap.raw"
    TEST_DATA_DIR = os.environ['HOME'] + "/Documents/code/phdtrack/phdtrack_project_3/data/graphs"
    #TEST_GRAPH_DATA_FILENAME = "graph_302-1644391327.gv"
    TEST_GRAPH_DATA_FILENAME = "467-1644391327-heap.gv"

    DATA_DIR_PATH = os.environ['HOME'] + "/Documents/code/phdtrack/phdtrack_data/Training/Training/scp/V_7_8_P1/16"
    ENDIANNESS = "little"

    def __init__(self, debug=False, **kwargs):
        self.DEBUG = debug

        if (
            self.check_path_exists(self.TEST_JSON_TEST_FILE_PATH) and
            self.check_path_exists(self.TEST_HEAP_DUMP_RAW_FILE_PATH) and
            self.check_path_exists(self.TEST_DATA_DIR) and
            self.check_path_exists(self.DATA_DIR_PATH)
        ):
            print("Program paths are OK.")
        else:
            print("Program paths are NOT OK.")
            exit(1)
    
    def check_path_exists(self, path: str):
        """
        Check if the path exists. Return True if it exists, False otherwise.
        """
        if not os.path.exists(path):
            print('WARNING: Path does not exist: %s' % path)
            return False
        return True



PARAMS = ProgramParams()