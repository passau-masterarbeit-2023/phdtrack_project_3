

from graph_data import GraphData
from graph_structures import *
from heap_dump_data import HeapDumpData
from mem_utils import *
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
    

    def __generate_key_data_from_json(self):
        """
        Generate a dictionary of key data from the JSON file.
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
        
        return addr_key_pairs
    

    def __get_all_addr_to_nodes(self, node_type: type[Node]):
        """
        Get all the Nodes (of given type) in the graph.
        """
        value_nodes: dict[int, node_type] = {}
        node: Node
        for node in self.graph:
            if isinstance(node, node_type):
                value_nodes[node.addr] = node
        return value_nodes
    

    def __annotate_graph_with_key_data(self):
        """
        Use JSON data to annotate the graph concerning the keys.
        """
        addr_key_pairs = self.__generate_key_data_from_json()

        # create a dictionary of address to node
        addr_to_value_node = self.__get_all_addr_to_nodes(ValueNode)
        
        # annotate the graph with the key data
        for key_addr, key_data in addr_key_pairs.items():
            if key_addr in addr_to_value_node.keys():
                value_nodes_of_key: list[ValueNode] = []

                # get all the ValueNodes that are part of the key
                for i in range(key_data.len // self.heap_dump_data.block_size):
                    addr = key_addr + i * self.heap_dump_data.block_size
                    value_nodes_of_key.append(
                        addr_to_value_node[addr]
                    )
                
                # concat the data of the ValueNodes
                key: bytes = b"".join([value_node.value for value_node in value_nodes_of_key])

                # watchdog: check if the key matches the key in the JSON
                if key != key_data.key:
                    print("WARNING: Key[%s] (%s) does not match key in JSON (%s)!" % (key_data.name, key.hex(), key_data.key.hex()))
                
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

    def __annotate_graph_with_session_state(self):
        """
        Annotate the graph with session state.
        """
        # create a dictionary of address to node
        addr_to_value_node = self.__get_all_addr_to_nodes(Node)

        # get the session state address from the JSON file
        session_state_addr = hex_str_to_addr(self.heap_dump_data.json_data["SESSION_STATE_ADDR"])
        print("SESSION_STATE_ADDR:", self.heap_dump_data.json_data["SESSION_STATE_ADDR"])

        # get the DataStructureNode that contains the session state
        session_state_node: ValueNode
        try:
            session_state_node = addr_to_value_node[session_state_addr]
        except KeyError:
            print("WARNING: Session state address (%s) not found in graph!" % hex(session_state_addr))
            print("session_state_addr:", hex(session_state_addr))
            return

        # get the ancestors and successors of the session state node
        ancestors: list[Node] = list(self.graph.predecessors(session_state_node))
        following_nodes: list[Node] = list(self.graph.successors(session_state_node))

        # remove the session state node from the graph
        self.graph.remove_node(session_state_node)

        # add the SessionStateNode to the graph
        session_state_node = SessionStateNode(
            addr=session_state_addr,
            value=session_state_node.value
        )
        self.graph_data.add_node_wrapper(session_state_node)

        # add edges from the ancestors and successors to the SessionStateNode
        for ancestor in ancestors:
            self.graph_data.add_edge_wrapper(ancestor, session_state_node)
        for following_node in following_nodes:
            self.graph_data.add_edge_wrapper(session_state_node, following_node)


    def annotate_graph(self):
        """
        Annotate the graph with data from the JSON file.
        """
        self.__annotate_graph_with_key_data()
        self.__annotate_graph_with_session_state()