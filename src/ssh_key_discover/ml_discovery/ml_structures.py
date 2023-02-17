from enum import Enum

class BalancingType(Enum):
    NONE = 0
    OVER = 1
    UNDER = 2

class ModelType(Enum):
    RFC = 0
    GRID_SEARCH_CV = 1

