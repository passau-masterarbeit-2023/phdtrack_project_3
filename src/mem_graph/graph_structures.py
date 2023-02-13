
from dataclasses import dataclass
from enum import Enum

# nodes (vertices)
@dataclass(frozen=True)
class Node:
    addr: int

    def __hash__(self):
        return hash(self.addr)

    def __eq__(self, other):
        return self.addr == other.addr

@dataclass(frozen=True)
class DataStructureNode(Node):
    byte_size : int

@dataclass(frozen=True)
class ValueNode(Node):
    value: bytes

@dataclass(frozen=True)
class PointerNode(Node):
    points_to: int

# edges (connections)
class Edge(Enum):
    DATA_STRUCTURE = 0
    POINTER = 1


