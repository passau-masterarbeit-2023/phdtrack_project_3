from dataclasses import dataclass
from params import ProgramParams
from mem_utils import addr_to_index, index_to_addr

import json
import os


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

        self.min_addr, self.max_addr = self.__get_min_max_addr_from_json(
            heap_dump_raw_file_path.replace("-heap.raw", ".json")
        )

    
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
                    print(heap_dump_lines[i].hex(), "int value:", int.from_bytes(heap_dump_lines[i], byteorder=self.params.ENDIANNESS, signed=False))
            
                print("Number of dump lines: %d" % len(heap_dump_lines), "of size:", block_size, "bytes")

        if len(heap_dump_lines) == 0:
            raise ValueError("No lines found in heap dump file: %s" % heap_dump_raw_file_path)

        return heap_dump_lines
    

    def __get_min_max_addr_from_json(
        self, 
        json_file_path: str,
    ):
        """
        Get the min and max address (real address) from the JSON file.
        """
        heap_start_addr = None

        with open(json_file_path, 'r') as json_file:
            json_data = json.load(json_file)
            heap_start_addr = bytes.fromhex(json_data["HEAP_START"])

        assert heap_start_addr is not None

        # get the min and max address of the heap
        min_addr = int.from_bytes(heap_start_addr, byteorder='big', signed=False) # HEAP_START
        max_addr = min_addr + len(self.blocks) * self.block_size

        if self.params.DEBUG:
            print("min_addr: %d, hex min_addr: %s" % (min_addr, hex(min_addr)))
            print("max_addr: %s, hex max_addr: %s" % (hex(min_addr), hex(max_addr)))

        return min_addr, max_addr






class GraphGenerator:
    """
    Generates a graph from a raw heap dump file.
    """

    params: ProgramParams
    heap_dump_data: HeapDumpData # WARN: allocated in generate_graph()

    def __init__(self, params: ProgramParams):
        self.params = params
        pass


    def generate_graph(
            self, 
            heap_dump_raw_file_path: str,
            pointer_byte_size: int
        ):
        """
        Generate a graph from a raw heap dump file.
        """

        pointers_to_values: dict[int, int] = {}

        # get the heap dump data
        self.heap_dump_data = HeapDumpData(
            heap_dump_raw_file_path=heap_dump_raw_file_path,
            block_size=pointer_byte_size,
            params=self.params,
        )

        # go through all the potential pointers in the heap dump
        counter = 0
        for i, potential_ptr in enumerate(self.heap_dump_data.blocks):

            potential_ptr_int  = self.__is_pointer(potential_ptr)
            if potential_ptr_int is not None:


            # check is the potential pointer is in range of the heap
            
                current_ptr_addr = index_to_addr(i, min_addr, self.params.POINTER_BYTE_SIZE)

                # add potential pointer to dict
                pointers_to_values[current_ptr_addr] = potential_ptr_int
                
                counter += 1

        if counter > 0:
            pointers_to_values = remove_unique_vertice_graphs(pointers_to_values)
            end_pointers_to_data = get_end_graph_data_str(pointers_to_values, blocks, min_addr) # data values at end of pointer graphs

            # open .gv file
            save_file_path = os.path.join(
                self.params.TEST_DATA_DIR, 
                str(os.path.basename(heap_dump_raw_file_path)).replace('.raw', '.gv')
            )

            # save the graph to file
            write_graphs_to_file(save_file_path, pointers_to_values, end_pointers_to_data)

            print("Writing graph to file: %s done." % self.params.TEST_DATA_DIR + self.params.TEST_GRAPH_DATA_FILENAME)
            print("Nb of found potential pointers: %d" % counter)
            print("Nb of non-unique-vertice-graph vertices : %d" % len(pointers_to_values))
        else:
            print("No potential pointers found in heap dump file: %s" % heap_dump_raw_file_path)




    def __is_pointer(self, data: bytes | int):
        """
        Check if an address is a pointer. 
        If it is, return the pointed address.
        """
        potential_ptr_int: int
        if isinstance(data, int):
            potential_ptr_int = data
        else:
            potential_ptr_int = int.from_bytes(
                data, byteorder=self.params.ENDIANNESS, signed=False
            )

        # check if the potential pointer is in range of the heap
        is_ptr = (
            potential_ptr_int >= self.heap_dump_data.min_addr and 
            potential_ptr_int <= self.heap_dump_data.max_addr
        )
        if is_ptr:
            return potential_ptr_int
        else:
            return None
    

    def __is_memalloc_header(self, data: bytes):
        """
        Check if an address is a memory allocation header.
        If it is, return the memalloc_header value.
        """
        
    