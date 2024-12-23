"""
`CommonNodes.py` module
Implements `Node` objects over the `INode` interface and `Edge` objects over the `IEdge` interface.

@author nrdc
@version 1.1
@date 2024-12-20
"""

from src.datastructures.primitives.NodicBasis import IEdge, INode, IGraph, GraphException, NodeException
from typing import Any, List, Tuple, Set;

class BasicNode(INode):
    """
    A `Node` for `Graph`-like structures, including trees.
    
    Attributes
    ----------
    value : Any
        The value of the node.
    identifier : int
        The identifier of the node.
    """
    def __init__(self, value: Any, identifier: int = 0) -> None:
        """
        Initializes a new `Node` object with the given value and identifier.

        Parameters
        ----------
        value : Any
            The value of the node.
        identifier : int, optional
            The identifier of the node, defaults to 0.
        """
        super().__init__(value, identifier);
        return;
    
    def __str__(self) -> str:
        return f"Node[id={self.identifier}value={self.value}]";
    
    def __repr__(self) -> str:
        return f"Node[id={self.identifier}value={self.value}]";
    
    def __eq__(self, other: "Node") -> bool:
        if self.identifier == other.identifier and self.value != other.value:
            raise NodeException.raise_repeated_node_error(self, other);
        return self.identifier == other.identifier and self.value == other.value;
    
    def __hash__(self) -> int:
        return hash((self.identifier, self.value));
    
    def __ne__(self, other: "Node") -> bool:
        return not self.__eq__(other);
    
    def __lt__(self, other: "Node") -> bool:
        return self.value < other.value;
    
    def __gt__(self, other: "Node") -> bool:
        return self.value > other.value;
    
    def __le__(self, other: "Node") -> bool:
        return self.value <= other.value;
    
    def __ge__(self, other: "Node") -> bool:
        return self.value >= other.value;


class BasicEdge(IEdge):
    """
    An `Edge` for `Graph`-like structures, including trees.
    
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
        super().__init__(source, target);
        self.weight = weight;
        return;
    
    def __str__(self) -> str:
        return f"({self.source}, {self.target}, [w={self.weight}])";
    
    def __eq__(self, other: "IEdge") -> bool:
        return self.source == other.source and self.target == other.target and self.weight == other.weight;
    
    def __hash__(self) -> int:
        return hash((self.source, self.target, self.weight));
    
    def __ne__(self, other: "IEdge") -> bool:
        return not self.__eq__(other);


class BasicGraph(IGraph):
    """
    A general `Graph` superclass for `Graph`-like structures, including trees.
    
    Attributes
    ----------
    nodes : Set[Node]
        The set of nodes in the graph.
    edges : Set[Edge]
        The set of edges in the graph.
    attributes : Dict[str, Any]
        The set of attributes in the graph.
    """
    
    def __init__(self) -> None:
        """
        Initializes a new empty `Graph` object.
        
        The graph is initialized with an empty set of nodes and edges.
        """
        self.nodes : Set[INode] = set();
        self.edges : Set[IEdge] = set();
        self.attributes : dict[str, Any] = dict();
        return;
        
    @staticmethod
    def from_nodes(nodes: Set[INode], edges: Set[IEdge]) -> "IGraph":
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
        G : BasicGraph = BasicGraph();
        G.nodes = nodes;
        G.edges = edges;
        return G;
    
    def degree(self, node: INode) -> int:
        """
        Returns the degree of the given node in the graph.
        
        Parameters
        ----------
        node : Node
            The node whose degree is to be calculated.
        
        Returns
        -------
        int
            The degree of the node.
        """
        return len([edge for edge in self.edges if edge.source == node or edge.target == node]);
    
    def neighbors(self, node: INode, distance: int = 1) -> Set[INode]:
        """
        Returns the neighbors of the given node in the graph, from 1 to a given distance.
        
        Parameters
        ----------
        node : Node
            The node whose neighbors are to be calculated.
        distance : int, optional
            The maximum distance from the node. Default is 1.
        
        Returns
        -------
        Set[Node]
            The set of neighbors of the node.
        """
        if distance <= 0: return set();
        
        explored : Set[INode] = set();
        frontier : List[INode] = [node];
        nodes : List[Tuple[INode, int]] = [];
        curr_distance : int = 0;
        
        for i in range(distance):
            for node in frontier:
                for edge in self.edges:
                    if edge.source == node and edge.target not in explored:
                        nodes.append((edge.target, curr_distance + 1));
                        explored.add(edge.target);
            curr_distance += 1;
            frontier = [node[0] for node in nodes];
            nodes = [];
            
        return set(node[0] for node in nodes);
        
        

    def exist_path(self, source: INode, target: INode) -> bool:
        """
        Checks if a path exists between the given source and target nodes in the graph.
        
        Parameters
        ----------
        source : Node
            The source node of the path.
        target : Node
            The target node of the path.
        
        Returns
        -------
        bool
            True if a path exists, False otherwise.
        """
        explored : Set[INode] = set();
        frontier : List[INode] = [source];
        
        while frontier:
            node = frontier.pop(0);
            if node == target:
                return True;
            explored.add(node);
            for edge in self.edges:
                if edge.source == node and edge.target not in explored:
                    frontier.append(edge.target);
        return False;


