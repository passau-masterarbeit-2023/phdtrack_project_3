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