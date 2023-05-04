from .graph_structures import Node, PointerNode, ValueNode

def addr_to_index(addr: int, min_addr: int, block_size: int) -> int:
    """
    Convert an address to an integer index inside block list.
    """
    index: int = (addr - min_addr) // block_size
    return index


def index_to_addr(index: int, min_addr: int, block_size: int) -> int:
    """
    Convert an integer index inside block list to an address.
    """
    addr: int = index * block_size + min_addr
    return addr

def hex_str_to_addr(hex_str: str) -> int:
    """
    Convert a hex string to an address.
    """
    byte_addr = bytes.fromhex(hex_str)
    return int.from_bytes(byte_addr, byteorder='big', signed=False)

def is_pointer(data: bytes | int, min_addr: int, max_addr: int, endianness: str):
        """
        Check if an address is a pointer. 
        If it is, return the pointed address.
        """
        potential_ptr_int: int
        if isinstance(data, int):
            potential_ptr_int = data
        else:
            potential_ptr_int = int.from_bytes(
                data, byteorder=endianness, signed=False
            )

        # check if the potential pointer is in range of the heap
        is_ptr = (
            potential_ptr_int >= min_addr and 
            potential_ptr_int <= max_addr
        )
        if is_ptr:
            return potential_ptr_int
        else:
            return None


def create_node_from_bytes(block: bytes, addr: int, min_addr: int, max_addr: int, endianness: str) -> Node:
    """
    Get the node from the data.
    NOTE: Remember that all addresses are relative to the heap, and converted to absolute addresses as int.
    """
    potential_ptr = is_pointer(block, min_addr, max_addr, endianness)
    if potential_ptr is not None:
        node = PointerNode(
            addr,
            potential_ptr
        )
    else: # this is a data block
        node = ValueNode(
            addr,
            block
        )
    
    return node