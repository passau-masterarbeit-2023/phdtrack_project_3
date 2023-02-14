from dataclasses import dataclass
from graph_structures import *

from params import ProgramParams
from mem_utils import *

import json
import os
import networkx as nx

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

        graph = nx.DiGraph()

        # get the heap dump data
        self.heap_dump_data = HeapDumpData(
            heap_dump_raw_file_path=heap_dump_raw_file_path,
            block_size=pointer_byte_size,
            params=self.params,
        )
        
        self.__data_structure_step(pointer_byte_size, graph)
        self.__pointer_step(graph)

        return graph
    

    def __is_pointer_wrapper(self, data: bytes | int):
        """
        Wrapper for is_pointer.
        """
        return is_pointer(data, self.heap_dump_data.min_addr, self.heap_dump_data.max_addr, self.params.ENDIANNESS)
    
    def __get_node_from_bytes_wrapper(self, data: bytes, addr: int):
        """
        Wrapper for get_node_from_bytes.
        """
        return get_node_from_bytes(data, addr, self.heap_dump_data.min_addr, self.heap_dump_data.max_addr, self.params.ENDIANNESS)


    def __get_node_from_bytes_wrapper_index(self, data: bytes, block_index: int):
        """
        Wrapper for get_node_from_bytes.
        """
        addr = self.heap_dump_data.index_to_addr_wrapper(block_index)
        return self.__get_node_from_bytes_wrapper(data, addr)
    

    def __data_structure_step(self, pointer_byte_size: int, graph: nx.DiGraph):
        """
        Parse all data structures step. Don't follow pointers yet.
        """

        def pass_null_blocks(index: int):
            """
            Pass null blocks.
            """
            while (
                index < len(self.heap_dump_data.blocks) and # check if index is in bounds
                self.heap_dump_data.blocks[index] == b'\x00' * pointer_byte_size
            ):
                index += 1
            return index
        
        # generate data structures and iterate over them
        block_index = 0
        while block_index < len(self.heap_dump_data.blocks):
            # pass null blocks
            block_index = pass_null_blocks(block_index)

            # get the data structure
            data_structure_block_size = self.__parse_datastructure(block_index, graph)

            # update the block index by leaping over the data structure
            block_index += data_structure_block_size + 1 

    def __pointer_step(self, graph: nx.DiGraph):
        """
        Parse all pointers step.
        """
        # create a dictionary of address to node
        addr_to_node: dict[int, Node] = {}
        for node in graph:
            addr_to_node[node.addr] = node

        def parse_pointer(node: PointerNode):
            """
            Parse a pointer node.
            """
            # check if the pointer points to a node in the graph
            current_pointer_node: Node = node
            while isinstance(current_pointer_node, PointerNode):
                if node.points_to not in addr_to_node:
                    
                    # create a new node
                    pointed_node = self.__get_node_from_bytes_wrapper(
                        self.heap_dump_data.blocks[self.heap_dump_data.addr_to_index_wrapper(node.addr)],
                        node.points_to
                    )

                    # add the node to the graph
                    graph.add_node(pointed_node)

                    # add the node to the dictionary
                    addr_to_node[node.points_to] = pointed_node

                    # add the edge
                    graph.add_edge(node, pointed_node, label=Edge.POINTER)

                    # next iteration
                    current_pointer_node = pointed_node
                else:
                    # get the node from the dictionary, and add the edge
                    pointed_node = addr_to_node[node.points_to]
                    graph.add_edge(node, pointed_node, label=Edge.POINTER) 

                    # no more iterations
                    break

        # get all pointer nodes
        all_pointer_nodes: list[PointerNode] = []
        for node in graph:
            if isinstance(node, PointerNode):
                all_pointer_nodes.append(node)

        for node in all_pointer_nodes:
            parse_pointer(node)
            print("pointer node:", node)


    def __get_memalloc_header(self, data: bytes):
        """
        get the malloc header (number of byte allocated + 1)
        """
        memalloc_header_int = int.from_bytes(
            data, byteorder="little", signed=False
        )
        return memalloc_header_int



    def __parse_datastructure(self, startBlockIndex : int, graph : nx.DiGraph):
        """
        Parse the data structure from a given block and populate the graph.
        WARN: We don't follow the pointers in the data structure. This is done in a second step.
        :return: The number of blocks in the data structure.
        If the data structure is not valid, return 0, since there no data structure to leap over.
        """
        # precondition: the block at startBlockIndex is not the last block of the heap dump or after
        if startBlockIndex >= len(self.heap_dump_data.blocks) - 1:
            return 0 # this is not a data structure, no need to leap over it

        # get the size of the data structure from malloc header
        # NOTE: the size given by malloc header is the size of the data structure + 1
        datastructure_size = self.__get_memalloc_header(self.heap_dump_data.blocks[startBlockIndex]) - 1

        # check if nb_blocks_in_datastructure is an integer
        tmp_nb_blocks_in_datastructure = datastructure_size / self.heap_dump_data.block_size
        if tmp_nb_blocks_in_datastructure % 1 != 0:
            if self.params.DEBUG:
                print("tmp_nb_blocks_in_datastructure:", tmp_nb_blocks_in_datastructure)
                print("The data structure size is not a multiple of the block size, at block index: %d" % startBlockIndex)
            return 0 # this is not a data structure, no need to leap over it

        # get the number of blocks in the data structure as an integer
        nb_blocks_in_datastructure = int(tmp_nb_blocks_in_datastructure)

        # check if the data structure is complete, i.e. if the data structure is still unclosed after at the end of the heap dump
        if startBlockIndex + nb_blocks_in_datastructure >= len(self.heap_dump_data.blocks):
            if self.params.DEBUG:
                print("The data structure is not complete, at block index: %d" % startBlockIndex)
            return 0
    
        # check that the data structure is not empty, i.e. that it contains at least one block
        # It cannot also be composed of only one block, since the first block is the malloc header,
        # and a data structure cannot be only the malloc header.
        if nb_blocks_in_datastructure < 2:
            if self.params.DEBUG:
                print("The data structure is too small (%d blocks), at block index: %d" % (nb_blocks_in_datastructure, startBlockIndex))
            return 0
        
        datastructure_node = DataStructureNode(
            self.heap_dump_data.index_to_addr_wrapper(startBlockIndex), 
            datastructure_size
        )
        graph.add_node(datastructure_node)

        for block_index in range(startBlockIndex + 1, startBlockIndex + nb_blocks_in_datastructure):
            node = self.__get_node_from_bytes_wrapper_index(self.heap_dump_data.blocks[block_index], block_index)
            graph.add_node(node)
            # add edge to the graph
            graph.add_edge(
                datastructure_node, 
                node,
                label=Edge.DATA_STRUCTURE
            )
        
        return nb_blocks_in_datastructure

            
            

        