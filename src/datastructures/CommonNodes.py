"""
`CommonNodes.py` module
Implements `Node` objects over the `INode` interface and `Edge` objects over the `IEdge` interface.

@author nrdc
@version 1.1
@date 2024-12-20
"""

from src.datastructures.primitives.NodicBasis import IEdge, INode, IGraph, GraphException, NodeException
from typing import Any, List, Tuple, Set;
from src.operators.ElementarNodicOperators import order

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
        
    @property
    def order(self) -> int:
        """
        Returns the order of a `Graph` object, which is the number of nodes in the graph.

        Returns:
            int: The order of the graph.
        """
        return len(self.nodes);
    
    @property
    def size(self) -> int:
        """
        Returns the size of a `Graph` object, which is the number of edges in the graph.

        Returns:
            int: The size of the graph.
        """
        return len(self.edges);
    
    @property
    def chromatic_number(self) -> int:
        """
        Returns the chromatic number of a `Graph` object, which is the maximum degree of any node in the graph.

        Returns:
            int: The chromatic number of the graph.
        """
        return max(self.degree(node) for node in self.nodes);
    
    def distance(self, source: INode, target: INode) -> int:
        """
        Returns the distance between two nodes in the graph.
        
        Parameters
        ----------
        source : Node
            The source node.
        target : Node
            The target node.
        
        Returns
        -------
        int
            The distance between the nodes.
        """
        return len(self.shortest_path(source, target));
    
    def shortest_path(self, source: INode, target: INode) -> List[INode]:
        """
        Returns the shortest path between two nodes in the graph.
        
        Parameters
        ----------
        source : Node
            The source node.
        target : Node
            The target node.
        
        Returns
        -------
        List[Node]
            The shortest path between the nodes.
        """
        path : List[INode] = [source];
        while path[-1] != target:
            path += [node for edge in self.edges if edge.source == path[-1] for node in [edge.target, edge.source] if node not in path];
        return path;
    
    def get_edges(self, node: INode) -> Set[IEdge]:
        """
        Given a `Node` in the graph, returns the set of edges that connect to that node.
        
        Parameters
        ----------
        node : Node
            The node whose edges are to be retrieved.
        
        Returns
        -------
        Set[Edge]
            The set of edges that connect to the node.
        """
        if node in self.nodes:
            return {edge for edge in self.edges if edge.source == node or edge.target == node};
        else:
            raise ValueError("The given node is not in the graph.");
        
    def get_nodes(self, edge: IEdge) -> Set[INode]:
        """
        Given an `Edge` in the graph, returns the set of nodes that are connected by that edge.
        
        Parameters
        ----------
        edge: IEdge
            The edge whose nodes are to be retrieved.
            
        Returns
        -------
        Set[Node]
            The set of nodes that are connected by the edge.
        """
        if edge in self.edges:
            if edge.source not in self.nodes or edge.target not in self.nodes:
                raise ValueError("The given edge is not in the graph.");
            else:
                return {edge.source, edge.target};
        else:
            raise ValueError("The given edge is not in the graph.");
        
