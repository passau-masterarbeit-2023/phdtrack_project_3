from .graph_structures import *

from ..params import ProgramParams
from .mem_utils import *

import json

class HeapDumpData:
    """
    Wrapper class for heap dump data.
    """
    params: ProgramParams

    block_size: int
    blocks: list[bytes]
    heap_dump_raw_file_path: str
    min_addr: int # int version of HEAP_START
    max_addr: int

    json_data: dict[str, str] # loaded json 

    def __init__(
        self, 
        heap_dump_raw_file_path: str,
        block_size: int,
        params: ProgramParams,
    ):
        self.params = params
        self.block_size = block_size
        self.heap_dump_raw_file_path = heap_dump_raw_file_path

        self.blocks = self.__generate_blocks_from_heap_dump(
            heap_dump_raw_file_path, block_size
        )
        self.__get_json_data(
            heap_dump_raw_file_path.replace("-heap.raw", ".json")
        )
        self.min_addr, self.max_addr = self.__get_min_max_addr()

    def addr_to_index_wrapper(self, addr: int) -> int:
        """
        Wrapper for addr_to_index.
        """
        return addr_to_index(addr, self.min_addr, self.block_size)
    
    def index_to_addr_wrapper(self, index: int) -> int:
        """
        Wrapper for index_to_addr.
        """
        return index_to_addr(index, self.min_addr, self.block_size)
    
    def __get_json_data(self, json_file_path: str):
        """
        Read the JSON file associated with the raw heap dump file,
        and store it.
        """
        with open(json_file_path, 'r') as json_file:
            self.json_data = json.load(json_file)
        

    def __generate_blocks_from_heap_dump(
        self, 
        heap_dump_raw_file_path: str,
        block_size: int,
    ):
        """
        From a given heap dump raw file, generate a list of blocks.
        Split the heap dump into blocks of block_size bytes.
        :return: a list of blocks.
        """
        heap_dump_lines: list[bytes] = []

        with open(heap_dump_raw_file_path, 'rb') as f:
            heap_dump = f.read()

            # split the heap dump into lines of POINTER_BYTE_SIZE bytes
            heap_dump_lines = [heap_dump[i:i+block_size] for i in range(0, len(heap_dump), block_size)]
            
            # print some lines
            if self.params.DEBUG: 
                for i in range(100, 105):
                    print(heap_dump_lines[i].hex(), "int value:", int.from_bytes(heap_dump_lines[i], byteorder=self.params.PTR_ENDIANNESS, signed=False))
            
                print("Number of dump lines: %d" % len(heap_dump_lines), "of size:", block_size, "bytes")

        if len(heap_dump_lines) == 0:
            raise ValueError("No lines found in heap dump file: %s" % heap_dump_raw_file_path)

        return heap_dump_lines
    

    def __get_min_max_addr(self):
        """
        Get the min and max address (real address) from the JSON file.
        WARN: Need to have the JSON file loaded first.
        """
        assert self.json_data is not None

        # get the min and max address of the heap
        min_addr = hex_str_to_addr(self.json_data["HEAP_START"])
        max_addr = min_addr + len(self.blocks) * self.block_size

        if self.params.DEBUG:
            print("min_addr: %d, hex min_addr: %s" % (min_addr, hex(min_addr)))
            print("max_addr: %s, hex max_addr: %s" % (hex(min_addr), hex(max_addr)))

        return min_addr, max_addr
    



