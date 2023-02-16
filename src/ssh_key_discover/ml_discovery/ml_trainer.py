
from concurrent.futures import ThreadPoolExecutor
import os
import pickle
import tqdm
from typing import Any
from sklearn.ensemble import RandomForestClassifier

from .ml_utils import time_measure
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

    def load_files_and_generate_samples_and_labels(self, filepaths: list[str]) -> tuple[list[list[int]], list[int]]:
        """
        Load the samples and labels from the files.
        """
        samples: list[list[int]] = [] # list of vectors of features
        labels: list[int] = [] # list of labels

        def load_and_generate_samples_and_lables_for_one_file(
                filepath: str, 
                threadId: int, 
                nb_threads: int
            ):
            """
            Load the samples and labels from one file.
            """
            print(f"[{threadId}/{nb_threads}] Loading samples and labels from {filepath}")

            graph_data = GraphData(
                self.params,
                filepath,
                self.params.BLOCK_BYTE_SIZE
            )
            graph_analyser = GraphAnalyser(graph_data)
            if self.params.DEBUG:
                print("Annotating graph...")
            graph_analyser.annotate_graph()
            if self.params.DEBUG:
                print("Cleaning graph...")
            graph_analyser.clean_graph()

            # generate the samples and labels
            if self.params.DEBUG:
                print("Generating samples and labels...")
            graph_embedding = GraphEmbedding(graph_data, self.params.BASE_EMBEDDING_DEPTH)
            current_addr_to_samples = graph_embedding.generate_embedded_samples()
            current_addr_to_labels = graph_embedding.generate_labels()

            return current_addr_to_samples, current_addr_to_labels

        # multi-threaded loading and generation of samples and labels
        with ThreadPoolExecutor(max_workers=self.params.MAX_WORKERS) as executor:
            results = executor.map(
                load_and_generate_samples_and_lables_for_one_file, 
                filepaths,
                range(len(filepaths)),
                [len(filepaths)] * len(filepaths)
            )
            for i, (current_addr_to_samples, current_addr_to_labels) in enumerate(results):
                for addr, sample in current_addr_to_samples.items():
                    label = current_addr_to_labels[addr]
                    # save the sample and label
                    samples.append(sample)
                    labels.append(label)
            
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

    def save_samples_and_labels(self, samples: list[list[int]], labels: list[int]):
        """
        Save the samples and labels to a file.
        """
        samples_and_labels_file_path = os.path.join(
            self.params.SAMPLES_AND_LABELS_DATA_DIR_PATH, 
            "samples_and_labels_training.pkl"
        )
        with open(samples_and_labels_file_path, 'wb') as file:
            pickle.dump((samples, labels), file)
    
    def load_samples_and_labels(self) -> tuple[list[list[int]], list[int]]:
        """
        Load the samples and labels from a file.
        """
        samples_and_labels_file_path = os.path.join(
            self.params.SAMPLES_AND_LABELS_DATA_DIR_PATH, 
            "samples_and_labels_training.pkl"
        )
        with open(samples_and_labels_file_path, 'rb') as file:
            samples, labels = pickle.load(file)
        return samples, labels

    def train(self, filepaths: list[str]):
        """
        Train the machine learning model.
        """
        samples : list[list[int]] = [] # list of vectors of features 
        labels : list[int] = [] # list of labels

        if self.params.LOAD_SAMPLES_AND_LABELS_FROM_FILE:
            with time_measure('load_samples_and_labels_from_file'):
                samples, labels = self.load_samples_and_labels()
        else:
            with time_measure('load_files_and_gen_samples_and_labels'): 
                samples, labels = self.load_files_and_generate_samples_and_labels(filepaths)
            
            # save the samples and labels to a file
            self.save_samples_and_labels(samples, labels)

        # initialize the classifier[:10]
        clf = RandomForestClassifier(random_state=0, n_jobs=-1)

        # fit the classifier to the training data, use multi-threading
        print("Fitting the classifier...")
        with time_measure('fit_classifier'):
            clf.fit(samples, labels)

        # save the model
        self.__save_model(clf, "random_forest_classifier_1_depth_5.pkl")