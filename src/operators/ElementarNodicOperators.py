"""
`ElementarNodicOperators.py` module
Implements operators over `Node`, `Edge` and `Graph` objects.

@author nrdc
@version 1.1
@date 2024-12-22
"""

from itertools import product, permutations, combinations;
from src.datastructures.primitives.NodicBasis import INode, IEdge, IGraph, GraphException, NodeException;
from typing import List, Set, Tuple, DefaultDict, TypeVar, Any;
from src.operators.ElementarNodicOperators import order


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
        
    Methods
    -------
    __init__(self, nodes: Set[Node], edges: Set[MEdge])
        Initializes a new `Multigraph` object from the given set of nodes and edges.
    __add__(self, other: Any)
        Adds the given object to the `Multigraph` object.
    __sub__(self, other: Any)
        Subtracts the given object from the `Multigraph` object.
    __mul__(self, other: Any)
        Multiplies the `Multigraph` object by the given object.
    __pow__(self, other: Any)
        Raises the `Multigraph` object to the given power.
    __eq__(self, other: "Multigraph")            
        Checks if the `Multigraph` object is equal to the given object.
    __hash__(self)
        Returns the hash value of the `Multigraph` object.
    __str__(self)
        Returns a string representation of the `Multigraph` object.
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
    
    def __div__(self, other: Any) -> "Multigraph":
        """
        Division of a Graph by `Node`, `Edge` or `Multigraph`.
        
        Parameters
        ----------
        other : Node, Edge or Multigraph
            The node, edge or multigraph to divide the graph by.
        
        Returns
        -------
        Multigraph
            The result of the division.
        """
        if isinstance(other, IEdge or MEdge):
            if other.source not in self.nodes or other.target not in self.nodes: raise GraphException("The source or target node of the edge is not in the graph.");
            else:
                return Multigraph(self.nodes, self.edges - {other});
        elif isinstance(other, INode):
            if other not in self.nodes: raise GraphException("The node is not in the graph.");
            else:
                return Multigraph(self.nodes - {other}, self.edges);
        elif isinstance(other, IGraph):    
            if isinstance(other, Multigraph):
                return Multigraph(self.nodes - other.nodes, self.edges - other.edges);
            else:
                raise GraphException("The other graph is not a multigraph.");
        else:
            raise GraphException("The other object is not a node, edge or multigraph.");
    
    def __mul__(self, other: Any) -> "Multigraph":
        """
        Multiplication of a Graph by `Node`, `Edge` or `Multigraph`.
        
        Parameters
        ----------
        other : Node, Edge or Multigraph
            The node, edge or multigraph to multiply the graph by.
        
        Returns
        -------
        Multigraph
            The result of the multiplication.
        """
        if isinstance(other, IEdge or MEdge):
            if other.source not in self.nodes or other.target not in self.nodes: raise GraphException("The source or target node of the edge is not in the graph.");
            else:
                return Multigraph(self.nodes, self.edges + {other});
        elif isinstance(other, INode):
            if other not in self.nodes: raise GraphException("The node is not in the graph.");
            else:
                return Multigraph(self.nodes, self.edges);
        elif isinstance(other, IGraph):    
            if isinstance(other, Multigraph):
                return Multigraph(self.nodes + other.nodes, self.edges + other.edges);
            else:
                raise GraphException("The other graph is not a multigraph.");
        else:
            raise GraphException("The other object is not a node, edge or multigraph.");
    
    def complement(self) -> "Multigraph":
        """
        Returns the complement of the graph.
        
        Returns
        -------
        Multigraph
            The complement of the graph.
        """
        possible_edges = set(combinations(self.nodes, 2));
        return Multigraph(self.nodes, possible_edges - self.edges);
    
    def copy(self) -> "Multigraph":
        """
        Returns a copy of the graph.
        
        Returns
        -------
        Multigraph
            The copy of the graph.
        """
        return Multigraph(self.nodes.copy(), self.edges.copy());
    
    def incidence_matrix(self) -> List[List[int]]:
        """
        Returns the incidence matrix of the graph.
        
        Returns
        -------
        List[List[int]]
            The incidence matrix of the graph.
        """
        matrix = [];
        for node in self.nodes:
            row = [];
            for edge in self.edges:
                if node in edge:
                    row.append(1);
                else:
                    row.append(0);
            matrix.append(row);
        return matrix;
    
    def adjacency_matrix(self) -> List[List[int]]:
        """
        Returns the adjacency matrix of the graph.
        
        Returns
        -------
        List[List[int]]
            The adjacency matrix of the graph.
        """
        matrix = [];
        for node in self.nodes:
            row = [];
            for other_node in self.nodes:
                if node == other_node:
                    row.append(0);
                elif node in Multigraph({node, other_node}, self.edges):
                    row.append(1);
                else:
                    row.append(0);
            matrix.append(row);
        return matrix;
    
    def __repr__(self) -> str:
        return self.__str__();
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Multigraph):
            return self.nodes == other.nodes and self.edges == other.edges;
        else:
            return False;
    
    def __hash__(self) -> int:
        return hash((self.nodes, self.edges));
    
    def order(self) -> int:
        return len(self.nodes);
    
    def size(self) -> int:
        return len(self.edges);
    
    def empty(self) -> bool:
        return len(self.nodes) == 0;
    
    def __len__(self) -> int:
        return len(self.edges);
    
    def __iter__(self):
        return iter(self.edges);
    
    def __contains__(self, item: Any) -> bool:
        if isinstance(item, IEdge or MEdge):
            return item in self.edges;
        elif isinstance(item, INode):
            return item in self.nodes;
        return False;
          
    def __str__(self) -> str:
        return f"Multigraph(nodes={self.nodes}, edges={self.edges})";
    
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
        nodes = set();
        edges = set();
        for i, row in enumerate(matrix):
            for j, value in enumerate(row):
                if value == 1:
                    nodes.add(INode(i));
                    nodes.add(INode(j));
                    edges.add(MEdge(INode(i), INode(j)));
        return Multigraph.from_nodes(nodes, edges);