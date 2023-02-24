

import subprocess
from .graph_data import GraphData
from .graph_structures import *
from .heap_dump_data import HeapDumpData
from .mem_utils import *
from ..params import *

import networkx as nx


class GraphAnalyser:
    """
    Class to analyse the graph.
    """
    graph_data: GraphData

    # aliases
    graph: nx.DiGraph
    params: ProgramParams
    heap_dump_data: HeapDumpData | None = None

    # important nodes
    ssh_struct_node: Node

    def __init__(self, graph_data: GraphData):
        self.graph_data = graph_data

        # aliases
        self.graph = self.graph_data.graph
        self.heap_dump_data = self.graph_data.heap_dump_data
        self.params = self.graph_data.params
    
    ########## JSON EXPLOITATION ##########

    def __generate_key_data_from_json(self):
        """
        Generate a dictionary of key data from the JSON file.
        """
        if self.heap_dump_data is None:
            raise Exception("HeapDumpData is None")
        
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
        self.params.COMMON_LOGGER.debug("Nb of keys in JSON: %d" % len(addr_key_pairs))
        
        return addr_key_pairs
    

    def __annotate_graph_with_key_data(self):
        """
        Use JSON data to annotate the graph concerning the keys.
        """
        if self.heap_dump_data is None:
            raise Exception("HeapDumpData is None")
        
        addr_key_pairs = self.__generate_key_data_from_json()

        # create a dictionary of address to node
        addrs_of_value_nodes = self.graph_data.get_all_addr_from_node_type(ValueNode)
        
        # annotate the graph with the key data
        for key_addr, key_data in addr_key_pairs.items():
            if key_addr in addrs_of_value_nodes:
                value_nodes_of_key: list[ValueNode] = []

                # get all the ValueNodes that are part of the key
                for i in range(key_data.len // self.heap_dump_data.block_size):
                    addr = key_addr + i * self.heap_dump_data.block_size
                    value_nodes_of_key.append(
                        self.graph_data.get_node(addr)
                    )
                
                # concat the data of the ValueNodes
                key: bytes = b"".join([value_node.value for value_node in value_nodes_of_key])

                # watchdog: check if the key matches the key in the JSON
                if key != key_data.key:
                    self.params.COMMON_LOGGER.warning("WARNING: Key[%s] (%s) does not match key in JSON (%s)!" % (key_data.name, key.hex(), key_data.key.hex()))
                
                # create the KeyNode
                key_node = KeyNode(
                    value=value_nodes_of_key[0].value,
                    addr=key_addr,
                    key=key,
                    key_data=key_data
                )

                # replace the first ValueNode in the graph, keep the rest
                self.graph_data.replace_node_by_new_one(
                    value_nodes_of_key[0], 
                    key_node
                )

            else:
                self.params.COMMON_LOGGER.warning("WARNING: Key address (%s) not found in graph!" % hex(key_addr))

    def __annotate_graph_with_json_ptr(
            self, 
            ptr_addr_hex: str, 
            annotation_type: type[PointerNode]
    ):
        """
        Annotate the graph with session state.
        """
        # get the session state address from the JSON file
        pointer_addr = hex_str_to_addr(ptr_addr_hex)
        self.params.COMMON_LOGGER.debug(f"{annotation_type}:", ptr_addr_hex)

        # get the PointerNode
        pointer = self.graph_data.get_node(pointer_addr)
        if pointer is None or not isinstance(pointer, PointerNode):
            self.params.COMMON_LOGGER.warning(f"WARNING: {annotation_type} pointer not found in graph!")
            return

        # replace the SessionStateNode in the graph
        annotated_pointer = annotation_type(
            addr=pointer.addr,
            points_to=pointer.points_to
        )
        self.graph_data.replace_node_by_new_one(
            pointer, 
            annotated_pointer
        )
    
        return annotated_pointer
    
    ########## GRAPH  ##########


    def annotate_graph(self):
        """
        Annotate the graph with data from the JSON file.
        """
        if self.heap_dump_data is None:
            raise Exception("HeapDumpData is None")

        self.__annotate_graph_with_key_data()
        self.ssh_struct_node = self.__annotate_graph_with_json_ptr(
            self.heap_dump_data.json_data["SSH_STRUCT_ADDR"],
            SSHStructNode
        )

        self.__annotate_graph_with_json_ptr(
            self.heap_dump_data.json_data["SESSION_STATE_ADDR"],
            SessionStateNode
        )

    def clean_graph(self):
        """
        Clean the graph.
        """
        if self.ssh_struct_node is not None:
            self.__clean_graph_of_useless_subgraphs(self.ssh_struct_node)
    

    def __clean_graph_of_useless_subgraphs(self, node_addr: Node):
        """
        Clean the graph. Keep only the connected subgraph which contains the specified node.
        """
        # create undirected copy of the graph
        undirected_graph = self.graph.to_undirected()

        # get the connected subgraph
        node_connected_component = nx.node_connected_component(undirected_graph, node_addr.addr)

        # remove all nodes that are not in the connected subgraph
        all_node_addrs: list[int] = [node for node in self.graph] # keep a fixed set of nodes
        for node_addr in all_node_addrs:
            if node_addr not in node_connected_component:
                self.graph.remove_node(node_addr)
    
    def visualize_graph(self, file_name: str = None):
        """
        Visualize the graph.
        """
        # filter out ValueNodes from graph
        filtered_graph = self.graph.copy()
        for node_addr in self.graph.nodes.keys():
            node = self.graph_data.get_node(node_addr)
            if (isinstance(node, ValueNode)):
                if not isinstance(node, IMPORTANT_VALUE_NODE_SUBTYPES):
                    filtered_graph.remove_node(node_addr)
                else:
                    self.params.COMMON_LOGGER.info("IMPORTANT VALUE NODE: %s of type %s" % (node, type(node)))

        # generate graphviz file
        if file_name is None:
            if self.heap_dump_data is None:
                raise Exception("HeapDumpData is None")
            file_name = self.heap_dump_data.heap_dump_raw_file_path.split("/")[-1].replace(".raw", ".gv")
        outfile_path = self.params.TEST_DATA_DIR + "/" + file_name
        nx.nx_agraph.write_dot(filtered_graph, outfile_path)

        # generate graph image
        # with open(outfile_path, 'r') as f:
        #     dot_graph_data = f.read()
        #     graph_png_file_path = outfile_path.replace('.gv', '.png')
        #     s = graphviz.Source(dot_graph_data)
        #     s.render(outfile=graph_png_file_path, format='png', view=True)

        # run sfdp command on graphviz file to generate graph image
        process = subprocess.Popen(
            ["sfdp", "-Gsize=67!", "-Goverlap=prism", "-Tpng", outfile_path, "-o", outfile_path.replace('.gv', '-sfdp.png')],
        )
        process.wait()
