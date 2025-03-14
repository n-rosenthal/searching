""" src/functionals/GraphProtocols.py
Defines protocols for graph classes.

Protocols for nodes:
--------------------
    -   Sizeable
        Has a `degree()` method that returns the degree of the node.
    -   Parentable
        Has a `parent` field that returns the parent of the node.

Protocols for graphs:
---------------------
    -   Valency
        Has `maxdegree()` and `mindegree()` methods tha return the maximum and minimum degree of the graph.
    -   Weighted
        Associates to each edge a weight.
    -   Labeled
        Associates to each edge a label.
"""

from typing import Protocol, TypeVar, Any;

TEdge = TypeVar("TEdge");

class Sizeable(Protocol):
    """
    The `Sizeable` protocol defines a class that has a `degree()` method that returns the degree of the node. Also defines `neighbors` field that returns the neighbors of the node.
    
    If this protocol is implemented over
        -   a `TNode` object, the `degree()` method returns the degree of the node.
    
    Else, the protocol has no meaning.
    """
    neighbors: list;
    
    def degree(self) -> int:
        """
        Returns the degree of the node.
        
        Returns
        -------
        int
            The degree of the node.
        """
        ...;
        
class Parentable(Protocol):
    """
    The `Parentable` protocol defines a class that has a `parent` field that returns the parent of the node.
    
    Attributes
    ----------
    parent : TNode
        The parent node of the node.
        
    Raises
    ------
    NotImplementedError
        If the parent is not of type Node.
    """
    TNode = TypeVar("TNode", bound="Parentable");
    parent: "TNode";
    
    def __init__(self, value: Any, node_id: int, parent: "TNode") -> None:
        ...;
    
class Valency(Protocol):
    """
    The `Valency` protocol defines a class that has `maxdegree()` and `mindegree()` methods that return the maximum and minimum degree of the graph.
    """
    def maxdegree(self) -> int:
        """
        Returns the maximum degree of the graph.
        
        Returns
        -------
        int
            The maximum degree of the graph.
        """
        ...;
        
    def mindegree(self) -> int:
        """
        Returns the minimum degree of the graph.
        
        Returns
        -------
        int
            The minimum degree of the graph.
        """
        ...;
        
class Weighted(Protocol):
    """
    The `Weighted` protocol defines a method for setting and getting the weight of an edge.
    This requires that the `edges` field of the graph to be now of type `set[tuple[TEdge, float]]`, whereas `TEdge` is a typevar for `tuple[TNode, TNode]`.
    
    Attributes
    ----------
    edges : set[tuple[TEdge, float]]
        The edges of the graph.
        
    Raises
    ------
    NotImplementedError
        If the edges are not of type `list[tuple[TEdge, float]]`.
    """
    TEdge = TypeVar("TEdge");
    TNode = TypeVar("TNode");
    edges: set[tuple[TEdge, float]];
    
    def __init__(self, nodes: set[TNode] = set(), edges: set[tuple[TEdge, float]] = set()) -> None:
        ...;
        
    def setWeight(self, edge: TEdge, weight: float) -> None:
        ...;
        
    def getWeight(self, edge: TEdge) -> float:
        ...;
        
class UnionAssociative(Protocol):
    """
    The `UnionAssociative` protocol defines that given u, v, w objects, we have
        u + (v + w) = (u + v) + w = (u + w) + v, for all u, v, w of Protocol<T>.
        
    Given two `TGraph`s G1 and G2, we have that
        G3 = G1 + G2 = G2 + G1
    """
    TGraph = TypeVar("TGraph");
    
    def __add__(self, other: "TGraph") -> "TGraph":
        ...;
        
    def __radd__(self, other: "TGraph") -> "TGraph":
        ...;
        
    def __iadd__(self, other: "TGraph") -> "TGraph":
        ...;
        
    def __ior__(self, other: "TGraph") -> "TGraph":
        ...;
        
    def __or__(self, other: "TGraph") -> "TGraph":
        ...;