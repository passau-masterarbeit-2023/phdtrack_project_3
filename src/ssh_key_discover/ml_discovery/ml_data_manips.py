from .ml_utils import time_measure
from ..params import ProgramParams
from .graph_embedding import GraphEmbedding
from ..mem_graph.graph_analyser import GraphAnalyser
from ..mem_graph.graph_data import GraphData

from concurrent.futures import ThreadPoolExecutor
import pickle
import os
from typing import Any


def load_files_and_generate_samples_and_labels(
        params: ProgramParams,
        filepaths: list[str],
    ) -> tuple[list[list[int]], list[int]]:
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
                params,
                filepath,
                params.BLOCK_BYTE_SIZE
            )
            graph_analyser = GraphAnalyser(graph_data)
            if params.DEBUG:
                print("Annotating graph...")
            graph_analyser.annotate_graph()
            if params.DEBUG:
                print("Cleaning graph...")
            graph_analyser.clean_graph()

            # generate the samples and labels
            if params.DEBUG:
                print("Generating samples and labels...")
            graph_embedding = GraphEmbedding(graph_data, params.BASE_EMBEDDING_DEPTH)
            current_addr_to_samples = graph_embedding.generate_embedded_samples()
            current_addr_to_labels = graph_embedding.generate_labels()

            return current_addr_to_samples, current_addr_to_labels

        # multi-threaded loading and generation of samples and labels
        with ThreadPoolExecutor(max_workers=params.MAX_WORKERS) as executor:
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


def save_model(params: ProgramParams, clf: Any, model_file_name: str):
        """Save the model to a file."""
        model_file_path = os.path.join(params.MODELS_DIR_PATH, model_file_name)
        with open(model_file_path, 'wb') as file:
            pickle.dump(clf, file)
    

def load_model(params: ProgramParams, model_file_name: str):
    """Load the model from a file."""
    model_file_path = os.path.join(params.MODELS_DIR_PATH, model_file_name)
    with open(model_file_path, 'rb') as file:
        clf = pickle.load(file)
    return clf


def save_samples_and_labels(
    params: ProgramParams, 
    samples: list[list[int]], 
    labels: list[int],
    save_file_name: str
):
    """
    Save the samples and labels to a file.
    """
    samples_and_labels_file_path = os.path.join(
        params.SAMPLES_AND_LABELS_DATA_DIR_PATH, 
        save_file_name
    )
    with open(samples_and_labels_file_path, 'wb') as file:
        pickle.dump((samples, labels), file)


def load_samples_and_labels(
    params: ProgramParams,
    save_file_name: str
) -> tuple[list[list[int]], list[int]]:
    """
    Load the samples and labels from a file.
    """
    samples_and_labels_file_path = os.path.join(
        params.SAMPLES_AND_LABELS_DATA_DIR_PATH, 
        save_file_name
    )
    with open(samples_and_labels_file_path, 'rb') as file:
        samples, labels = pickle.load(file)
    return samples, labels


def get_samples_and_labels(
    params: ProgramParams,
    save_file_name: str,
    filepaths: list[str]
):
    """
    Get the samples and labels.
    :return: samples, a list of vectors of features 
    :return: labels, corresponding list of labels
    """
    samples : list[list[int]] = [] # list of vectors of features 
    labels : list[int] = [] # list of labels

    # check that save file exists
    samples_and_labels_file_path = os.path.join(
        params.SAMPLES_AND_LABELS_DATA_DIR_PATH,
        save_file_name
    )
    if os.path.exists(samples_and_labels_file_path):
        print(f"Loading samples and labels from {samples_and_labels_file_path}")
        with time_measure('load_samples_and_labels_from_file'):
            samples, labels = load_samples_and_labels(
                params, save_file_name
            )
    else:
        print(f"Generating samples and labels from {len(filepaths)} heap dump files")
        with time_measure('load_files_and_gen_samples_and_labels'): 
            samples, labels = load_files_and_generate_samples_and_labels(
                params, filepaths
            )
        
        # save the samples and labels to a file
        save_samples_and_labels(
            params, samples, labels, save_file_name
        )

    return samples, labels