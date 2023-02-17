

from ssh_key_discover.params import ProgramParams
from ssh_key_discover.ml_discovery.ml_pipelines import BalancingType, ModelType, Pipelines

import subprocess
import graphviz
import networkx as nx

def main():
    print("Running program...")

    params = ProgramParams(debug=False)

    pipelines = Pipelines(params)
    pipelines.training_pipeline(
        modelType=ModelType.GridSearchCV,
        balancingType=BalancingType.OVER,
        training_dir_path=params.TRAINING_DATA_DIR_PATH
    )
    pipelines.testing_pipeline(
        modelType=ModelType.GridSearchCV,
        balancingType=BalancingType.OVER,
        testing_dir_path=params.TESTING_DATA_DIR_PATH
    )





if __name__ == "__main__":
    main()
