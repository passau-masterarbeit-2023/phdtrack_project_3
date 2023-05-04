
from typing import Iterator
from ..mem_graph.graph_data import GraphData
from ..mem_graph.graph_structures import *
from ..params import ProgramParams
from ..mem_graph.mem_utils import *
from ..mem_graph.heap_dump_data import HeapDumpData

from attr import frozen
import networkx as nx

@frozen
class WeightingEdgeNode():
    """
    Represent a Node in the graph to simplify the computation of the ancestors (i.e. if the edge have a weight of 8, it means that the 
    pointed node have 8 depth ancestors).
    """
    weight : int
    firstTimeIndex : int # index of the first time we see this node in the ancestors list
    node : Node
    ancestorNode : Node # the node

    def __hash__(self):
        return int(str(hash(self.ancestorNode.addr)) + str(hash(self.node.addr)))

    def __eq__(self, other):
        return self.ancestorNode.addr == other.ancestorNode.addr and self.node.addr == other.node.addr
    
    def __str__(self):
        return f"WeightingEdgeNode(weight={self.weight}, firstTimeIndex={self.firstTimeIndex}, node={self.node}, ancestorNode={self.ancestorNode})"

class GraphEmbedding:
    graph_data: GraphData
    depth: int # hyperparameter, affect the length of the vectors

    # aliases
    graph: nx.DiGraph
    heap_dump_data: HeapDumpData
    params: ProgramParams

    def __init__(self, graph_data: GraphData, depth: int):
        self.graph_data = graph_data
        self.depth = depth

        # aliases
        self.graph = self.graph_data.graph
        if self.graph_data.heap_dump_data is not None:
            self.heap_dump_data = self.graph_data.heap_dump_data
        self.params = self.graph_data.params

    #------------ vectorization ------------

    def __get_first_weighting_edge_node(self, node: Node, ancestorNode : Node, actualIndex : int) -> WeightingEdgeNode:
        """
        Get the first WeightingEdgeNode of a node.
        """
        edge_weight : int = self.graph.get_edge_data(ancestorNode.addr, node.addr)["weight"]
        return WeightingEdgeNode(edge_weight, actualIndex, node, ancestorNode)
        

    def __vectorize_ancestor(self, node: ValueNode) -> list[int]:
        """
        Vectorize the ancestor of a node.
        """
        try:
            assert isinstance(node, ValueNode)
        except AssertionError:
            raise TypeError("The node must be a ValueNode. Found: %s, for node %s" % (type(node), node))

        current_ancestors: set[WeightingEdgeNode] = set() # ancestors to discover at step N
        previous_ancestors: set[WeightingEdgeNode] = set() # ancestors discovered at step N-1
        previous_ancestors.add(WeightingEdgeNode(0, 0, node, node)) # init 

        vector: list[int] = []
        self.params.COMMON_LOGGER.debug("Vectorizing node %s" % node)
        for i in range(1, self.depth + 1):
            # get the ancestors of the previous ancestors
            current_ancestors = set()
            for previous_ancestor in previous_ancestors:
                # if we haven't reached the number of ancestor of this edge, we keep it
                if previous_ancestor.weight > (i - previous_ancestor.firstTimeIndex):
                    current_ancestors.add(previous_ancestor)
                else:
                    predecessors: list[int] = self.graph.predecessors(previous_ancestor.ancestorNode.addr)
                    for predecessor in predecessors:
                        current_ancestors.add(self.__get_first_weighting_edge_node(previous_ancestor.ancestorNode, self.graph_data.get_node(predecessor), i))

            # feature computations
            count_data_structures = 0
            count_pointers = 0

            self.params.COMMON_LOGGER.debug(f"current_ancestors at {i}:   [see below]")
            for current_ancestor in current_ancestors:
                self.params.COMMON_LOGGER.debug(f"current_ancestor: {current_ancestor}")
                ancestor_node = current_ancestor.ancestorNode
                if isinstance(ancestor_node, DataStructureNode):
                    count_data_structures += 1
                elif isinstance(ancestor_node, PointerNode):
                    count_pointers += 1
            self.params.COMMON_LOGGER.debug("End of current_ancestors.")

            # add the features to the vector
            vector.append(count_data_structures)
            vector.append(count_pointers)

            previous_ancestors = current_ancestors

        return vector
    
    def __vectorize_DTN(self, node: ValueNode) -> list[int]:
        """ 
        Vectorize a node, with data structure data.
        put the following information in the order :
        - allocation size in the DTN
        - offset of the VN in the DTN
        - number of pointers in the DTN
        - number of VN in the DTN
        """

        data_structure_node : DataStructureNode = self.graph_data.get_data_structure_from_child(node, False)
        if data_structure_node is None:
            return [0] * 4 # if the node is not in a data structure, we return a vector of 0

        feature : list[int] = []
        feature.append(data_structure_node.byte_size)
        feature.append((node.addr - data_structure_node.addr) / self.params.BLOCK_BYTE_SIZE)

        # use DTN statistics for the number of pointers and value nodes
        feature.append(data_structure_node.nb_pointer_nodes)
        feature.append(data_structure_node.nb_value_nodes)
        
        #print(f"nb of children nodes: pn: {data_structure_node.nb_pointer_nodes}, vn: {data_structure_node.nb_value_nodes}")

        return feature    
    

    def __vectorize_node(self, node: ValueNode) -> list[int]:
        """
        Vectorize a node.
        """
        import time
        # count time needed
        start_time = time.time()
        ancestor_vector = self.__vectorize_ancestor(node)
        end_time = time.time()
        self.params.COMMON_LOGGER.info("Ancestors vectorization time: %s" % (end_time - start_time))

        start_time = time.time()
        DTN_vector = self.__vectorize_DTN(node)
        end_time = time.time()
        self.params.COMMON_LOGGER.info("DTN vectorization time: %s" % (end_time - start_time))

        return ancestor_vector + DTN_vector

    #------------ generation ------------

    def generate_embedded_samples(self) -> dict[int, list[int]]:
        """
        Generates a dictionary of embedded samples, from addresses to vectors.
        NOTE: the depth is the number of ancestor levels to consider.
        """
        # get all the ValueNodes
        value_node_addrs: list[int] = self.graph_data.get_all_addr_from_node_type(ValueNode)

        # vectorize the nodes
        embedded_samples: dict[int, list[int]] = {}
        for value_node_addr in value_node_addrs:
            value_node = self.graph_data.get_node(value_node_addr)
            embedded_samples[value_node.addr] = self.__vectorize_node(value_node)
        
        return embedded_samples
    
    def generate_labels(self) -> dict[int, int]:
        """
        Generates a dictionary of labels, from addresses to labels. (if the graph has been analyzed)
        """
        # get all the ValueNodes
        value_node_addrs: list[int] = self.graph_data.get_all_addr_from_node_type(ValueNode)

        # generate the labels
        labels: dict[int, int] = {}
        for value_node_addr in value_node_addrs:
            value_node = self.graph_data.get_node(value_node_addr)
            if isinstance(value_node, KeyNode):
                labels[value_node.addr] = 1
            else:
                labels[value_node.addr] = 0
        
        return labels