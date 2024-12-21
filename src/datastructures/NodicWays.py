"""
`NodicWays.py` module
Implementation of Paths, Cycles and other iterable objects over `Node`, `Edge` and `Graph` objects.

@author nrdc
@version 1.1
@date 2024-12-21
"""

from src.datastructures.primitives.NodicBasis import INode, IEdge, IGraph, GraphException, NodeException
from typing import Any, List, Tuple, Set
from itertools import product, permutations, combinations
from src.datastructures.NodicAlgorithms import djikstra


class Walk:
    """
    A `Walk` is a finite sequence of `Edge`s that joins a sequence of `Node`s in a `Graph`.
    A `Walk` may have repeated `Node`s and `Edge`s.
    
    Attributes
    ----------
    nodes : List[Node]
        The nodes in the walk.
    edges : List[Edge]
        The edges in the walk.
    """
    def __init__(self, nodes: List[INode], edges: List[IEdge]) -> None:
        self.nodes = nodes;
        self.edges = edges;
        return;
    
    def __str__(self) -> str:
        return "->".join(map(str, zip(self.nodes, self.edges)));
    
    def __repr__(self) -> str:
        return self.__str__();
    
    def __eq__(self, other: "Walk") -> bool:
        return self.nodes == other.nodes and self.edges == other.edges;
    
    def __hash__(self) -> int:
        return hash((tuple(self.nodes), tuple(self.edges)));
    
    def __len__(self) -> int:
        return len(self.nodes);
    
    def __getitem__(self, index: int) -> Tuple[INode, IEdge]:
        return self.nodes[index], self.edges[index];
    
    def __iter__(self):
        return iter(zip(self.nodes, self.edges));
    
    def __reversed__(self):
        return reversed(zip(self.nodes, self.edges));
    
    def __contains__(self, item: Tuple[INode, IEdge]):
        return item in zip(self.nodes, self.edges);
    
    def __add__(self, other: "Walk") -> "Walk":
        return Walk(self.nodes + other.nodes, self.edges + other.edges);

class Trail(Walk):
    """
    A `Trail` is a finite sequence of `Edge`s that joins a sequence of `Node`s in a `Graph`.
    A `Trail` is a `Walk` that may have repeated `Node`s but does not have repeated `Edges`s.
    
    Attributes
    ----------
    nodes : List[Node]
        The nodes in the trail.
    edges : List[Edge]    
        The edges in the trail.
    """
    @staticmethod
    def is_trail(nodes: List[INode], edges: List[IEdge]) -> bool:
        """
        Returns True if the walk is a trail, i.e., if the list of edges has no duplicates.
        A trail is a walk that may have repeated nodes but does not have repeated edges.
        """
        return len(edges) == len(set(edges));
    
    def __init__(self, nodes: List[INode], edges: List[IEdge]) -> None:
        if self.is_trail(nodes, edges): super().__init__(nodes, edges);
        else: raise GraphException("The walk is not a trail.");
        return;
    
    def __str__(self) -> str:
        return "->".join(map(str, zip(self.nodes, self.edges)));
    
    def __repr__(self) -> str:
        return self.__str__();
    
class Path(Trail):
    """
    A `Path` is a finite sequence of `Edge`s that joins a sequence of `Node`s in a `Graph`.
    A `Path` is a `Trail` (therefore, also a `Walk`) that has no repeated `Node`s nor `Edge`s.
    
    Attributes
    ----------
    nodes : List[Node]
        The nodes in the path.
    edges : List[Edge]    
        The edges in the path.
    """
    @staticmethod
    def is_path(nodes: List[INode], edges: List[IEdge]) -> bool:
        """
        Returns True if the walk is a path, i.e., if the list of nodes and edges has no duplicates.
        A path is a walk that has no repeated nodes nor edges.
        """
        return len(nodes) == len(set(nodes)) and len(edges) == len(set(edges));
    
    def __init__(self, nodes: List[INode], edges: List[IEdge]) -> None:
        try:
            if self.is_path(nodes, edges): super().__init__(nodes, edges);
        except GraphException:
            raise GraphException("The walk is not a path.");
        return;
    
    def __str__(self) -> str:
        return "->".join(map(str, zip(self.nodes, self.edges)));
    
    def __repr__(self) -> str:
        return self.__str__();

def is_path(graph: IGraph, source: INode, target: INode) -> bool:
    """
    Returns True if the graph contains a path from the source to the target.
    
    Parameters
    ----------
    graph : Graph
        The graph.
    source : Node
        The source node.
    target : Node
        The target node.
    
    Returns
    -------
    bool
        True if the graph contains a path from the source to the target, False otherwise.
    """
    if source == target: return True;
    if source not in graph.nodes or target not in graph.nodes: raise GraphException("The source or target node is not in the graph.");
    #if source not in graph.edges or target not in graph.edges: raise GraphException("The source or target edge is not in the graph.");
    
    nodes : List[INode] = list(graph.nodes);
    edges : List[IEdge] = list(graph.edges);
    explored : Set[INode] = set();
    frontier : Set[INode] = {source};
    
    while len(frontier) > 0:
        node : INode = frontier.pop();
        if node == target: return True;
        explored.add(node);
        for edge in edges:
            if edge.source == node and edge.target not in explored:
                frontier.add(edge.target);
    return False;
    
def djikstra(graph: IGraph) -> Set[List[IEdge]]:
    """
    Returns all possible paths in a graph using Dijkstra's algorithm.
    
    Parameters
    ----------
    graph : Graph
        The graph.
    
    Returns
    -------
    Set[List[Edge]]
        A set of all possible paths in the graph.
    """
    paths : Set[List[IEdge]] = {[]};
    
    #   Paths of size 1
    for node in graph.nodes:
        for edge in graph.edges:
            if edge.source == node:
                paths.add([edge]);
    
    #   Paths of size 2
    for path in paths:
        for edge in graph.edges:
            if edge.target == path[-1].source:
                paths.add(path + [edge]);
    
    return paths;
    

