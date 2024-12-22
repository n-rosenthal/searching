"""
`ElementarNodicOperators.py` module
Implements operators over `Node`, `Edge` and `Graph` objects.

@author nrdc
@version 1.1
@date 2024-12-22
"""

from src.datastructures.primitives.NodicBasis import INode, IEdge, IGraph, GraphException, NodeException;
from typing import List, Set, Tuple, DefaultDict, TypeVar, Any;


def size(graph: IGraph) -> int:
    """
    Returns the number of nodes in the graph.
    
    Parameters
    ----------
    graph : Graph
        The graph.
    
    Returns
    -------
    int
        The number of nodes in the graph.
    """
    return len(graph.nodes);

def order(graph: IGraph) -> int:
    """
    Returns the number of edges in the graph.
    
    Paramenters
    ----------
    graph : Graph
        The graph.
    
    Returns
    -------
    int
        The number of edges in the graph.
    """
    return len(graph.edges);

def empty(graph: IGraph) -> bool:
    """
    Returns True if the graph is empty, False otherwise.
    
    Parameters
    ----------
    graph : Graph
        The graph.
    
    Returns
    -------
    bool
        True if the graph is empty, False otherwise.
    """
    return len(graph.nodes) == 0;

class MEdge(IEdge):
    """
    A `MEdge` is an `Edge` associated with a `multiplicity` field.
    
    Parameters
    ----------
    source : Node
        The source node of the edge.
    target : Node
        The target node of the edge.
    multiplicity : int
        The multiplicity of the edge.
    """
    def __init__(self, source: INode, target: INode, multiplicity: int) -> None:
        if multiplicity is None or multiplicity <= 0: raise GraphException("The multiplicity of the edge must be a non-negative integer.");
        else:
            self.source = source;
            self.target = target;
            self.multiplicity = multiplicity;
            return;

class Multigraph(IGraph):
    """
    A `Multigraph` is a `Graph` structure that accepts internal loops and parallel, multiple edges between any pair of `Node`s.
    
    Parameters
    ----------
    nodes : Set[Node]
        The set of nodes in the graph.
    edges : Set[MEdge]
        The set of edges in the graph.
    
    Attributes
    ----------
    nodes : Set[Node]
        The set of nodes in the graph.
    edges : Set[Edge]
        The set of edges in the graph.
    attributes : Set[Any]
        The set of attributes in the graph.
    """
    def __init__(self, nodes: Set[INode], edges: Set[MEdge]) -> None:
        self.nodes = nodes;
        self.edges = edges;
        return;
    
    def __add__(self, other: Any) -> "Multigraph":
        if isinstance(other, IEdge or MEdge):
            if other.source not in self.nodes or other.target not in self.nodes: raise GraphException("The source or target node of the edge is not in the graph.");
            else:
                self.edges.add(other);
                return self;
        elif isinstance(other, INode):
            if other in self.nodes: return;
            else:
                self.nodes.add(other);
                return self;
        elif isinstance(other, IGraph):
            if isinstance(other, Multigraph):
                self.nodes.update(other.nodes);
                self.edges.update(other.edges);
                return self;
            else:
                raise GraphException("The other graph is not a multigraph.");
            
    def __sub__(self, other: Any) -> "Multigraph":
        if isinstance(other, IEdge or MEdge):
            if other.source not in self.nodes or other.target not in self.nodes: raise GraphException("The source or target node of the edge is not in the graph.");
            else:
                self.edges.remove(other);
                return self;
        elif isinstance(other, INode):
            if other not in self.nodes: raise GraphException("The node is not in the graph.");
            else:
                self.nodes.remove(other);
                return self;
        elif isinstance(other, IGraph):
            if isinstance(other, Multigraph):
                self.nodes.difference_update(other.nodes);
                self.edges.difference_update(other.edges);
                return self;
            else:
                raise GraphException("The other graph is not a multigraph.");
            
    def __str__(self) -> str:
        return f"Multigraph(nodes={self.nodes}, edges={self.edges})";
    
    def incidence_matrix(self) -> List[List[int]]:
        """
        Returns the incidence matrix of the graph.
        
        Parameters
        ----------
        graph : Graph
            The graph.
        
        Returns
        -------
        List[List[int]]
            The incidence matrix of the graph.
        """
        matrix = [[0 for _ in range(len(self.nodes))] for _ in range(len(self.edges))];
        
        for i in range(len(self.nodes)):
            for j in range(len(self.edges)):
                if self.edges[j].source == self.nodes[i]:
                    matrix[j][i] = self.edges[j].multiplicity;
                elif self.edges[j].target == self.nodes[i]:
                    matrix[j][i] = -self.edges[j].multiplicity;
        return matrix;
    
    def adjacency_matrix(self) -> List[List[int]]:
        """
        Returns the adjacency matrix of the graph.
        
        Parameters
        ----------
        graph : Graph
            The graph.
        
        Returns
        -------
        List[List[int]]
            The adjacency matrix of the graph.
        """
        matrix = [[0 for _ in range(len(self.nodes))] for _ in range(len(self.nodes))];
        
        for i in range(len(self.nodes)):
            for j in range(len(self.edges)):
                if self.edges[j].source == self.nodes[i]:
                    matrix[i][self.nodes.index(self.edges[j].target)] = self.edges[j].multiplicity;
                elif self.edges[j].target == self.nodes[i]:
                    matrix[self.nodes.index(self.edges[j].source)][i] = self.edges[j].multiplicity;
        return matrix;
    
    @staticmethod
    def from_nodes(nodes: Set[INode], edges: Set[MEdge]) -> "Multigraph":
        """
        Creates a new `Graph` object from the given set of nodes and edges.
        
        Parameters
        ----------
        nodes : Set[Node]
            The set of nodes in the graph.
        edges : Set[Edge]
            The set of edges in the graph.
        
        Returns
        -------
        Graph
            The new `Graph` object.
        """
        G : Multigraph = Multigraph(nodes, edges);
        return G;
    
    @staticmethod
    def from_incidence_matrix(matrix: List[List[int]]) -> "Multigraph":
        """
        Creates a new `Graph` object from the given incidence matrix.
        
        Parameters
        ----------
        matrix : List[List[int]]
            The incidence matrix of the graph.
        
        Returns
        -------
        Graph
            The new `Graph` object.
        """
        G : Multigraph = Multigraph(set(), set());
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] != 0:
                    G += MEdge(G.nodes[j], G.nodes[i], matrix[i][j]);
        return G;    