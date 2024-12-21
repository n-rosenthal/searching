"""
Class definitions for primitive node structures and trees

@author nrdc
@version 1.1
@date 2024-12-20
"""
from typing import Any, List, Set
from random import random, randint, uniform;
from abc import ABCMeta, abstractmethod, ABC

class NodeException(Exception):
    def __init__(self, message: str = "") -> None:
        """
        Initializes a new `NodeException` object with the given message.

        Parameters
        ----------
        message : str, optional
            The message of the exception. Default is an empty string.
        """
        super().__init__(message);
        self.message = message;
        
    def __str__(self) -> str:
        return self.message;
    
    def __repr__(self):
        return self.__str__();
    
    @staticmethod
    def raise_error(message: str = "") -> None:
        raise NodeException(message);
    
    @staticmethod
    def raise_repeated_node_error(v: "INode", u: "INode") -> None:
        raise NodeException(f"Repeated node: {v} == {u}");

class GraphException(Exception):
    def __init__(self, message: str = "") -> None:
        """
        Initializes a new `GraphException` object with the given message.

        Parameters
        ----------
        message : str, optional
            The message of the exception. Default is an empty string.
        """
        super().__init__(message);
        self.message = message;
        
    def __str__(self) -> str:
        return self.message;
    
    def __repr__(self):
        return self.__str__();
    
    @staticmethod
    def raise_error(message: str = "") -> None:
        raise GraphException(message);
    
    @staticmethod
    def raise_invalid_edge_loop(v: str, u: str) -> None:
        """
        Raises a `GraphException` if an edge is added to a simple graph that would form an internal edge loop.

        Parameters
        ----------
        v : str
            The source node of the edge.
        u : str
            The target node of the edge.

        Raises
        ------
        GraphException
            If the edge is a loop (i.e., v == u).
        """
        raise GraphException(f"A simple graph cannot have an internal edge loop: {v} == {u}");

    def raise_inexistent_edge(self, v: str, _u: str = None):
        """
        Raises a `GraphException` if the edge does not exist in the graph.

        Parameters
        ----------
        v : str
            The source node of the edge.
        _u : str
            The target node of the edge, defaults to None.

        Raises
        ------
        GraphException
            If the edge does not exist in the graph.
        """

class INode(metaclass=ABCMeta):
    """
    Abstract base class for a `Node` object in graphs.
    """
    def __init__(self, value: Any, identifier: int = 0) -> None:
        """
        Initializes a new `Node` object with the given value.

        Parameters
        ----------
        value : Any
            The value of the node.
        identifier : int, optional
            The identifier of the node. Default is 0.
        """
        self.value = value;
        if identifier == 0:
            self.identifier = randint(0, 1000000);
        else:
            self.identifier = identifier;
        
    @abstractmethod
    def __str__(self) -> str:
        return str(self.value);
    
    def __repr__(self) -> str:
        return self.__str__();
    
    def __eq__(self, other: "INode") -> bool:
        return self.value == other.value;
    
    def __hash__(self) -> int:
        return hash(self.value);

class IEdge(metaclass=ABCMeta):
    """
    Abstract base class for an unweighted `Edge` object in graphs.
    
    A `Edge` object represents a connection between two nodes in a graph.
    
    Attributes
    ----------
    source : Node
        The source node of the edge.
    target : Node
        The target node of the edge.
   """
    def __init__(self, source: INode, target: INode) -> None:
        """
        Initializes a new `Edge` object with the given source and target nodes.

        Parameters
        ----------
        source : Node
            The source node of the edge.
        target : Node
            The target node of the edge.
        """
        if source == target:
            GraphException.raise_invalid_edge_loop(source.value, target.value);
            return;
        
        self.source = source;
        self.target = target;
        return;
    
    def __str__(self) -> str:
        return f"({self.source.value}, {self.target.value})";
    
    def __repr__(self) -> str:
        return self.__str__();
    
    def __eq__(self, other: "IEdge") -> bool:
        return self.source == other.source and self.target == other.target;
    
    def __hash__(self) -> int:
        return hash((self.source, self.target));

class WeightedEdge(IEdge):
    """
    A `WeightedEdge` object represents a weighted connection between two nodes in a graph.
    
    Attributes
    ----------
    source : Node
        The source node of the edge.
    target : Node
        The target node of the edge.
    weight : float
        The weight of the edge.
    """
    def __init__(self, source: INode, target: INode, weight: float = 1.) -> None:
        """
        Initializes a new `WeightedEdge` object with the given source, target, and weight.

        Parameters
        ----------
        source : Node
            The source node of the edge.
        target : Node
            The target node of the edge.
        weight : float
            The weight of the edge, defaults to 1.
        """
        super().__init__(source, target);
        self.weight = weight;
        return;
    
    def __str__(self) -> str:
        return f"({self.source.value}, {self.target.value})[w={self.weight})]";
    
    def __repr__(self) -> str:
        return self.__str__();
    
    def __eq__(self, other: "WeightedEdge") -> bool:
        return self.source == other.source and self.target == other.target and self.weight == other.weight;
    
    def __hash__(self) -> int:
        return hash((self.source, self.target, self.weight));
    
    def __lt__(self, other: "WeightedEdge") -> bool:
        return self.weight < other.weight;
    
    def __le__(self, other: "WeightedEdge") -> bool:
        return self.weight <= other.weight;
    
    def __gt__(self, other: "WeightedEdge") -> bool:
        return self.weight > other.weight;
    
    def __ge__(self, other: "WeightedEdge") -> bool:
        return self.weight >= other.weight;
    
class IGraph(metaclass=ABCMeta):
    """
    Abstract base class for the `Graph` classes.
    A `Graph` is a 3-uple (V, E, A) where:
    - V is a set of nodes
    - E is a set of edges
    - A is a set of attributes
    
    Attributes
    ----------
    nodes : Set[Node]
        The set of nodes in the graph.
    edges : Set[Edge]
        The set of edges in the graph.
    attributes : Set[Any]
        The set of attributes in the graph.
    """
    def __init__(self) -> None:
        """
        Initializes a new empty `Graph` object.
        
        The graph is initialized with an empty set of nodes, edges and attributes.
        """
        self.nodes : Set[INode] = set();
        self.edges : Set[IEdge] = set();
        self.attributes : Set[Any] = set();
        return;
    
    def __str__(self) -> str:
        return f"Graph(nodes={self.nodes}, edges={self.edges}, attributes={self.attributes})";
    
    def __repr__(self) -> str:
        return self.__str__();
    
    def __eq__(self, other: "IGraph") -> bool:
        return self.nodes == other.nodes and self.edges == other.edges and self.attributes == other.attributes;
    
    def __hash__(self) -> int:
        return hash((self.nodes, self.edges, self.attributes));
    
    def __len__(self) -> int:
        return len(self.nodes);