from ssh_key_discover.params import ProgramParams
from ssh_key_discover.ml_discovery.ml_pipelines import Pipelines
from ssh_key_discover.ml_discovery.ml_structures import ModelType, BalancingType 

import subprocess
import graphviz
import networkx as nx

def main():
    print("Running program...")

    params = ProgramParams()

    pipelines = Pipelines(params)
    pipelines.training_pipeline(
        modelType=params.MODEL_TYPE,
        balancingType=params.BALANCING_TYPE,
        training_dir_path=params.TRAINING_DATA_DIR_PATH
    )
    pipelines.testing_pipeline(
        modelType=params.MODEL_TYPE,
        balancingType=params.BALANCING_TYPE,
        testing_dir_path=params.TESTING_DATA_DIR_PATH
    )





if __name__ == "__main__":
    main()
