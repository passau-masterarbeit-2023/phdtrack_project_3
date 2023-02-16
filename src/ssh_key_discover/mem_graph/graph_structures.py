from attr import frozen, attrib
from enum import Enum

from abc import ABC


# nodes (vertices)
@frozen
class Node(ABC):
    addr: int
    color: str

    def __hash__(self):
        return hash(self.addr)

    def __eq__(self, other):
        return self.addr == other.addr

@frozen
class Filled(ABC):
    """
    Filled node.
    """
    pass


@frozen
class DataStructureNode(Node):
    byte_size : int
    color: str = attrib("blue")
    style: str = attrib("")

    def __str__(self):
        return f"DTN({hex(self.addr)})"


@frozen
class ValueNode(Node):
    """
    A value node is a node that contains a value
    which is not currently identified.
    """
    value: bytes
    color: str = attrib("grey")

    def __str__(self):
        return f"VN({hex(self.addr)})"

@frozen
class PointerNode(Node):
    """
    A pointer node is an identified ValueNode. 
    It do not need the value since it gives meaning to it.
    """
    points_to: int
    color: str = attrib("orange")

    def __str__(self):
        return f"PN({hex(self.addr)})"

@frozen
class SessionStateNode(PointerNode, Filled):
    color: str = attrib("red")

    def __str__(self):
        return f"SSN({hex(self.addr)})"

@frozen
class SSHStructNode(PointerNode, Filled):
    color: str = attrib("purple")

    def __str__(self):
        return f"SSHN({hex(self.addr)})"

# key stuff
# read the JSON file and get all pair of addresses and keys
@frozen
class KeyData:
    """
    Wrapper class for key data.
    """
    name: str
    key: bytes
    addr: bytes
    len: int
    real_len: int


@frozen
class KeyNode(ValueNode, Filled):
    """
    Composed of data from several ValueNodes.
    It contains the key data from both the heap dump and the JSON file.
    """
    key: bytes # found in heap dump
    key_data: KeyData # found in JSON file
    color: str = attrib("green")

    def __str__(self):
        return f"KN_{self.key_data.name[-1]}({hex(self.addr)})"

# edges (connections)
class Edge(Enum):
    DATA_STRUCTURE = 0
    POINTER = 1

    def __str__(self):
        if self == Edge.DATA_STRUCTURE:
            return "dts"
        elif self == Edge.POINTER:
            return "ptr"


# type lists
IMPORTANT_VALUE_NODE_SUBTYPES = (
    SessionStateNode,
    SSHStructNode,
    KeyNode
)
