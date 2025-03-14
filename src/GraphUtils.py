from primitives.TGraphBuilder import create_node
from typing import Any, TypeVar
from string import ascii_letters

__all__ = ["ascii_nodes"];

def ascii_nodes(n: int) -> list:
    """
    Returns a list of `n` nodes with values from the alphabet.
    
    Parameters
    ----------
    n : int
        The number of nodes to create.
    
    Returns
    -------
    list[TNode]
        A list of `n` nodes with values from the alphabet.
    
    Raises
    ------
    NotImplemented
        If `n` is greater than the number of letters in the alphabet.
    """
    if n > len(ascii_letters):
        raise NotImplemented(f"n must be less than {len(ascii_letters)}");
    return [create_node(ascii_letters[i - 1], i) for i in range(1, n + 1)];
