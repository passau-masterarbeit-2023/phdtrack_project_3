
import os
import pickle
from typing import Any
from sklearn.ensemble import RandomForestClassifier
from ..mem_graph.graph_data import GraphData
from ..mem_graph.graph_analyser import GraphAnalyser
from ..mem_graph.graph_structures import *
from ..params import ProgramParams
from ..mem_graph.mem_utils import *
from ..mem_graph.heap_dump_data import HeapDumpData
from .graph_embedding import GraphEmbedding

import networkx as nx

class MLTrainer:
    params: ProgramParams

    def __init__(self, params: ProgramParams):
        self.params = params

    def load_samples_and_labels(self, filepaths: list[str]) -> tuple[list[list[int]], list[int]]:
        """
        Load the samples and labels from the files.
        """
        samples: list[list[int]] = [] # list of vectors of features
        labels: list[int] = [] # list of labels

        for filepath in filepaths:
            graph_data = GraphData(
                self.params,
                filepath,
                self.params.BLOCK_BYTE_SIZE
            )
            graph_analyser = GraphAnalyser(graph_data)
            graph_analyser.annotate_graph()
            graph_analyser.clean_graph()

            graph_embedding = GraphEmbedding(graph_data, self.params.BASE_EMBEDDING_DEPTH)
            current_addr_to_samples = graph_embedding.generate_embedded_samples()
            current_addr_to_labels = graph_embedding.generate_labels()

            # generate similarly organized lists
            addr_ordered = sorted(current_addr_to_samples.keys())
            for addr in addr_ordered:
                samples.append(current_addr_to_samples[addr])
                labels.append(current_addr_to_labels[addr])
        
        return samples, labels

    def __save_model(self, clf: Any, model_file_name: str):
        """Save the model to a file."""
        model_file_path = os.path.join(self.params.MODELS_DIR_PATH, model_file_name)
        with open(model_file_path, 'wb') as file:
            pickle.dump(clf, file)
    
    def load_model(self, model_file_name: str) -> Any:
        """Load the model from a file."""
        model_file_path = os.path.join(self.params.MODELS_DIR_PATH, model_file_name)
        with open(model_file_path, 'rb') as file:
            clf = pickle.load(file)
        return clf

    def train(self, filepaths: list[str]):
        """
        Train the machine learning model.
        """
        samples, labels = self.load_samples_and_labels(filepaths)

        # initialize the classifier[:10]
        clf = RandomForestClassifier(random_state=0)

        # fit the classifier to the training data
        clf.fit(samples, labels)

        # save the model
        self.__save_model(clf, "random_forest_classifier_1_depth_5.pkl")