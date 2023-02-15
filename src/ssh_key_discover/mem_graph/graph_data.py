from .graph_structures import *
from ..params import ProgramParams
from .mem_utils import *
from .heap_dump_data import HeapDumpData

import networkx as nx


class GraphData:
    """
    Generates a graph from a raw heap dump file.
    """
    params: ProgramParams
    heap_dump_data: HeapDumpData # WARN: allocated in generate_graph()
    graph: nx.DiGraph

    def __init__(
            self, 
            params: ProgramParams,
            heap_dump_raw_file_path: str,
            pointer_byte_size: int
        ):
        """
        Generate a graph from a raw heap dump file.
        """
        self.params = params
        self.graph = nx.DiGraph()

        # get the heap dump data
        self.heap_dump_data = HeapDumpData(
            heap_dump_raw_file_path=heap_dump_raw_file_path,
            block_size=pointer_byte_size,
            params=self.params,
        )
        
        self.__data_structure_step(pointer_byte_size)
        self.__pointer_step()
    
    ########## WRAPPER FUNCTIONS ##########

    def __is_pointer_wrapper(self, data: bytes | int):
        """
        Wrapper for is_pointer.
        """
        return is_pointer(data, self.heap_dump_data.min_addr, self.heap_dump_data.max_addr, self.params.PTR_ENDIANNESS)
    
    def __get_node_from_bytes_wrapper(self, data: bytes, addr: int):
        """
        Wrapper for get_node_from_bytes.
        """
        return get_node_from_bytes(data, addr, self.heap_dump_data.min_addr, self.heap_dump_data.max_addr, self.params.PTR_ENDIANNESS)


    def __get_node_from_bytes_wrapper_index(self, data: bytes, block_index: int):
        """
        Wrapper for get_node_from_bytes.
        """
        addr = self.heap_dump_data.index_to_addr_wrapper(block_index)
        return self.__get_node_from_bytes_wrapper(data, addr)

    def add_node_wrapper(self, node: Node):
        """
        Wrapper for add_node. Add a node with its color to the graph.
        """
        if isinstance(node, Filled):
            self.graph.add_node(node, style="filled", color=node.color)
        else:
            self.graph.add_node(node, color=node.color)
    
    def add_edge_wrapper(self, node_start: Node, node_end: Node):
        """
        Wrapper for add_edge. Add an edge to the graph.
        """
        # get the type of the edge
        edge_type: Edge
        if isinstance(node_start, PointerNode):
            edge_type = Edge.POINTER
        elif isinstance(node_start, DataStructureNode):
            edge_type = Edge.DATA_STRUCTURE
        else:
            raise ValueError("Unknown node type: %s" % node_start)
        
        # case where a pointer points to a data structure
        # NOTE: a pointer never points to a DataStructureNode,
        # it always points to a ValueNode, and if this one is 
        # the first one after the data structure malloc header (DataStructureNode), 
        # then it means that the pointer points to the data structure.
        if isinstance(node_start, PointerNode):
            parent_data_structure = self.get_data_structure_from_first_children(node_end)

            if parent_data_structure is not None:
                node_end = parent_data_structure


        self.graph.add_edge(
            node_start, 
            node_end,
            label=edge_type
        )

    ########## UTILS ##########

    def get_all_addr_to_nodes(self, node_type: type[Node]):
        """
        Get all the Nodes (of given type) in the graph.
        """
        value_nodes: dict[int, node_type] = {}
        node: Node
        for node in self.graph:
            if isinstance(node, node_type):
                value_nodes[node.addr] = node
        return value_nodes
    
    def get_node(self, addr: int):
        """
        Get a node from its address.
        """
        node: Node
        for node in self.graph:
            if node.addr == addr:
                return node
        return None

    def replace_node_by_new_one(self, old_node: Node, new_node: Node):
        """
        Replace a node in the graph.
        """
        # get the ancestors and successors of the session state node
        ancestors: list[Node] = list(self.graph.predecessors(old_node))
        following_nodes: list[Node] = list(self.graph.successors(old_node))

        # remove the node from the graph
        self.graph.remove_node(old_node)

        # add the new node to the graph
        self.add_node_wrapper(new_node)

        # add edges from the ancestors and successors to the SessionStateNode
        for ancestor in ancestors:
            self.add_edge_wrapper(ancestor, new_node)
        for following_node in following_nodes:
            self.add_edge_wrapper(new_node, following_node)

    def get_data_structure_from_first_children(self, node: Node):
        """
        Get the data structure from the first children of a node.
        This means the function only returns a data structure if the node 
        is the first one after the data structure malloc header.
        """
        # get the ancestors of the node
        ancestors: list[Node] = list(self.graph.predecessors(node))

        preceding_data_structure: DataStructureNode | None = None
        for ancestor in ancestors:
            if (
                isinstance(ancestor, DataStructureNode) and
                # check if the node is the first one after the data structure malloc header
                ancestor.addr == node.addr - self.params.BLOCK_BYTE_SIZE
            ):
                preceding_data_structure = ancestor
                break
        return preceding_data_structure

    ########## LOGIC ##########
    
    def __data_structure_step(self, pointer_byte_size: int):
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
            data_structure_block_size = self.__parse_datastructure(block_index)

            # update the block index by leaping over the data structure
            block_index += data_structure_block_size + 1 

    def __pointer_step(self):
        """
        Parse all pointers step.
        """
        # create a dictionary of address to node
        addr_to_node: dict[int, Node] = {}
        node: Node
        for node in self.graph:
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
                    self.add_node_wrapper(pointed_node)

                    # add the node to the dictionary
                    addr_to_node[node.points_to] = pointed_node

                    # add the edge
                    self.add_edge_wrapper(node, pointed_node)

                    # next iteration
                    current_pointer_node = pointed_node
                else:
                    # get the node from the dictionary, and add the edge
                    pointed_node = addr_to_node[node.points_to]
                    self.add_edge_wrapper(node, pointed_node) 

                    # no more iterations
                    break

        # get all pointer nodes
        all_pointer_nodes: list[PointerNode] = []
        for node in self.graph:
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



    def __parse_datastructure(self, startBlockIndex : int):
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
        self.add_node_wrapper(datastructure_node)

        for block_index in range(startBlockIndex + 1, startBlockIndex + nb_blocks_in_datastructure):
            node = self.__get_node_from_bytes_wrapper_index(self.heap_dump_data.blocks[block_index], block_index)
            self.add_node_wrapper(node)
            self.add_edge_wrapper(datastructure_node, node)
        
        return nb_blocks_in_datastructure

