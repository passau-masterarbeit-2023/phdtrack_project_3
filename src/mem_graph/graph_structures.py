
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

    def __str__(self):
        return f"DTN({hex(self.addr)})"

@dataclass(frozen=True)
class ValueNode(Node):
    value: bytes

    def __str__(self):
        return f"VN({hex(self.addr)})"

@dataclass(frozen=True)
class PointerNode(Node):
    points_to: int

    def __str__(self):
        return f"PN({hex(self.addr)})"

# edges (connections)
class Edge(Enum):
    DATA_STRUCTURE = 0
    POINTER = 1

    def __str__(self):
        if self == Edge.DATA_STRUCTURE:
            return "dts"
        elif self == Edge.POINTER:
            return "ptr"


