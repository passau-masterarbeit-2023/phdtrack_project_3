

from ..mem_graph.graph_data import GraphData
from ..mem_graph.graph_structures import *
from ..params import ProgramParams
from ..mem_graph.mem_utils import *
from ..mem_graph.heap_dump_data import HeapDumpData

import networkx as nx

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
        self.heap_dump_data = self.graph_data.heap_dump_data
        self.params = self.graph_data.params

    def __vectorize_node(self, node: Node) -> list[int]:
        """
        Vectorize a node.
        """
        current_ancestors: set[Node] = set() # ancestors to discover at step N
        previous_ancestors: set[Node] = set([node]) # ancestors discovered at step N-1

        vector: list[int] = []

        for _ in range(self.depth):

            # get the ancestors of the previous ancestors
            current_ancestors = set()
            for ancestor in previous_ancestors:
                current_ancestors.add(self.graph.predecessors(ancestor))
        
            # feature computations
            count_data_structures = 0
            count_pointers = 0

            for ancestor in current_ancestors:
                if isinstance(ancestor, DataStructureNode):
                    count_data_structures += 1
                elif isinstance(ancestor, PointerNode):
                    count_pointers += 1
            
            # add the features to the vector
            vector.append(count_data_structures)
            vector.append(count_pointers)

            previous_ancestors = current_ancestors

        return vector


    
    def generate_embedded_samples(self) -> dict[int, list[int]]:
        """
        Generates a dictionary of embedded samples, from addresses to vectors.
        NOTE: the depth is the number of ancestor levels to consider.
        """

        # get all the ValueNodes
        value_nodes: list[ValueNode] = self.graph_data.get_all_addr_to_nodes(ValueNode).values()

        # vectorize the nodes
        embedded_samples: dict[int, list[int]] = {}
        for value_node in value_nodes:
            embedded_samples[value_node.addr] = self.__vectorize_node(value_node)
        
        return embedded_samples
    
    def generate_labels(self) -> dict[int, int]:
        """
        Generates a dictionary of labels, from addresses to labels. (if the graph has been analyzed)
        """
        # get all the ValueNodes
        value_nodes: list[ValueNode] = self.graph_data.get_all_addr_to_nodes(ValueNode).values()

        # generate the labels
        labels: dict[int, int] = {}
        for value_node in value_nodes:
            if isinstance(value_node, KeyNode):
                labels[value_node.addr] = 1
            else:
                labels[value_node.addr] = 0
        
        return labels