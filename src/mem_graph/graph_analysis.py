

from graph_data import GraphData
from graph_structures import *
from heap_dump_data import HeapDumpData
from params import *

import networkx as nx


class GraphAnalyser:
    """
    Class to analyse the graph.
    """
    graph_data: GraphData

    # aliases
    graph: nx.DiGraph
    heap_dump_data: HeapDumpData
    params: ProgramParams

    def __init__(self, graph_data: GraphData):
        self.graph_data = graph_data

        # aliases
        self.graph = self.graph_data.graph
        self.heap_dump_data = self.graph_data.heap_dump_data
        self.params = self.graph_data.params
    

    def annotate_graph_with_json(self):
        """
        Use JSON data to annotate the graph.
        """
        json_data = self.heap_dump_data.json_data # alias
        addr_key_pairs: dict[int, KeyData] = {} # key addr (int in base 16 - hex) -> key data (KeyData)

        # iterate over the keys in the JSON file
        for json_key_name in json_data:
            # match json key names that start with 'KEY_' and are followed by a single letter
            if json_key_name.startswith('KEY_') and len(json_key_name) == 5:
                real_key_addr = bytes.fromhex(json_data[json_key_name + "_ADDR"])
                addr_key_pairs[int.from_bytes(real_key_addr, byteorder='big', signed=False)] = KeyData(
                    name=json_key_name,
                    key=bytes.fromhex(json_data[json_key_name]),
                    addr=real_key_addr,
                    len=int(json_data[json_key_name + "_LEN"]),
                    real_len=int(json_data[json_key_name + "_REAL_LEN"])
                )

        # print nb of keys
        if self.params.DEBUG:
            print("Nb of keys in JSON: %d" % len(addr_key_pairs))

        # create a dictionary of address to node
        addr_to_node_value: dict[int, ValueNode] = {}
        node: Node
        for node in self.graph:
            if isinstance(node, ValueNode):
                addr_to_node_value[node.addr] = node
        
        # annotate the graph
        for key_addr, key_data in addr_key_pairs.items():
            if key_addr in addr_to_node_value.keys():
                value_nodes_of_key: list[ValueNode] = []

                # get all the ValueNodes that are part of the key
                for i in range(key_data.len // self.heap_dump_data.block_size):
                    addr = key_addr + i * self.heap_dump_data.block_size
                    value_nodes_of_key.append(
                        addr_to_node_value[addr]
                    )
                
                # concat the data of the ValueNodes
                key: bytes = b"".join([value_node.value for value_node in value_nodes_of_key])

                # create the KeyNode
                key_node = KeyNode(
                    addr=key_addr,
                    key=key,
                    key_data=key_data
                )

                # before removing the ValueNodes, get the ancestors of the ValueNodes
                ancestors: list[Node] = list(self.graph.predecessors(value_nodes_of_key[0]))

                # remove the ValueNodes from the graph
                for value_node in value_nodes_of_key:
                    self.graph.remove_node(value_node)
                
                # add the KeyNode to the graph
                self.graph_data.add_node_wrapper(key_node)

                # add edges from the ancestors to the KeyNode
                for ancestor in ancestors:
                    self.graph_data.add_edge_wrapper(ancestor, key_node)

            else:
                if self.params.DEBUG:
                    print("WARNING: Key address (%s) not found in graph!" % hex(key_addr))
