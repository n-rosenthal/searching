""" src/TGraphBuilder.py
Implements functions for easily creating TGraph objects (nodes and edges) and TGraph graphs:

Functions
---------
create_node(value: str, id: int) -> TNode
    Creates a node with the given value and id.

create_edge(v: TNode, w: TNode) -> TEdge
    Creates an edge between the given nodes v and w.
    

Also implements the `get_adjacency_list` and `get_adjacency_matrix` functions over lists of nodes and edges, or TGraph graphs.

Functions
---------
get_adjacency_list(nodes: list[Any] | list[TNode] | TGraph, edges: list[tuple[int, Any]] | list[TEdge]) -> AdjacencyList
    Creates an adjacency list from the given nodes and edges.

get_adjacency_matrix(nodes: list[Any] | list[TNode] | TGraph, edges: list[tuple[int, Any]] | list[TEdge]) -> AdjacencyMatrix
    Creates an adjacency matrix from the given nodes and edges.
"""

from primitives.datatypes.TGraph import TGraph, TEdge, TNode, getAdjacencyList, getAdjacencyMatrix, AdjacencyMatrix, AdjacencyList;
from typing import Any;

__all__ = ["create_node", "create_edge", "create_graph", "create_adjacency_list", "create_adjacency_matrix"];
__version__ = "1.0.0";
__author__ = "rdcn";
__status__ = "Development";
__import__ = "src.TGraphBuilder";


class TGraphFactory:
    """
    Factory class for creating TGraph objects (nodes and edges).
    """
    @staticmethod
    def create_node(value: str, id: int) -> TNode:
        """
        Creates a node with the given value and id.
        
        Parameters
        ----------
        value : str
            The value of the node.
        id : int
            The id of the node.
        
        Returns
        -------
        TNode
            The created node.
        """
        return TNode(value, id);
    
    @staticmethod
    def create_edge(v: TNode, w: TNode) -> TEdge:
        """
        Creates an edge between the given nodes v and w.
        
        Parameters
        ----------
        v : TNode
            The first node of the edge.
        w : TNode
            The second node of the edge.
        
        Returns
        -------
        TEdge
            The created edge.
        """
        return (v, w);

def create_node(value: str, id: int) -> TNode:
    """
    Creates a node with the given value and id.
    Invokes the `TGraphFactory.create_node` method.
    
    Parameters
    ----------
    value : str
        The value of the node.
    id : int
        The id of the node.
    
    Returns
    -------
    TNode
        The created node.
    """
    return TGraphFactory.create_node(value, id);

def create_edge(v: TNode, w: TNode) -> TEdge:
    """
    Creates an edge between the given nodes v and w.
    Invokes the `TGraphFactory.create_edge` method.
    
    Parameters
    ----------
    v : TNode
        The first node of the edge.
    w : TNode
        The second node of the edge.
    
    Returns
    -------
    TEdge
        The created edge.
    """
    return TGraphFactory.create_edge(v, w);


class TGraphBuilder:
    """
    Builder class for creating TGraph graph objects.
    """
    @staticmethod
    def create_graph(nodes: list[Any] | list[TNode], edges: list[tuple[int, Any]] | list[TEdge]) -> TGraph:
        """
        Creates a new `TGraph` object from the given nodes and edges.
        
        Parameters
        ----------
        nodes : list[Any] | list[TNode]
            The list of nodes for the graph. If the list contains non-`TNode` objects, they will be converted to `TNode` objects using `TGraphFactory.create_node`.
        edges : list[tuple[int, Any]] | list[TEdge]
            The list of edges for the graph. If the list contains non-`TEdge` objects, they will be converted to `TEdge` objects using `TGraphFactory.create_edge`.
        
        Returns
        -------
        TGraph
            The new `TGraph` object.
        """
        if all(isinstance(node, TNode) for node in nodes) and all(isinstance(edge, tuple) for edge in edges):
            return TGraph(nodes, edges);
        else:
            return TGraph(list(map(TGraphFactory.create_node, nodes)), list(map(TGraphFactory.create_edge, edges)));
        
    @staticmethod
    def create_adjacency_list(nodes: list[Any] | list[TNode], edges: list[tuple[int, Any]] | list[TEdge]) -> AdjacencyList:
        """
        Creates an adjacency list from the given nodes and edges.
        
        Parameters
        ----------
        nodes : list[Any] | list[TNode]
            The list of nodes for the graph. If the list contains non-`TNode` objects, they will be converted to `TNode` objects using `TGraphFactory.create_node`.
        edges : list[tuple[int, Any]] | list[TEdge]
            The list of edges for the graph. If the list contains non-`TEdge` objects, they will be converted to `TEdge` objects using `TGraphFactory.create_edge`.
        
        Returns
        -------
        AdjacencyList
            The adjacency list of the graph.
        """
        if all(isinstance(node, TNode) for node in nodes) and all(isinstance(edge, tuple) for edge in edges):
            return getAdjacencyList(edges);
        else:
            return getAdjacencyList(list(map(TGraphFactory.create_edge, edges)));
        
    @staticmethod
    def create_adjacency_matrix(nodes: list[Any] | list[TNode], edges: list[tuple[int, Any]] | list[TEdge]) -> AdjacencyMatrix:
        """
        Creates an adjacency matrix from the given nodes and edges.
        
        Parameters
        ----------
        nodes : list[Any] | list[TNode]
            The list of nodes for the graph. If the list contains non-`TNode` objects, they will be converted to `TNode` objects using `TGraphFactory.create_node`.
        edges : list[tuple[int, Any]] | list[TEdge]
            The list of edges for the graph. If the list contains non-`TEdge` objects, they will be converted to `TEdge` objects using `TGraphFactory.create_edge`.
        
        Returns
        -------
        AdjacencyMatrix
            The adjacency matrix of the graph.
        """
        if all(isinstance(node, TNode) for node in nodes) and all(isinstance(edge, tuple) for edge in edges):
            return getAdjacencyMatrix(edges);
        else:
            return getAdjacencyMatrix(list(map(TGraphFactory.create_edge, edges)));

def build_graph(nodes: list[Any] | list[TNode], edges: list[tuple[int, Any]] | list[TEdge]) -> TGraph:
    """
    Creates a new `TGraph` object from the given nodes and edges.
    
    Parameters
    ----------
    nodes : list[Any] | list[TNode]
        The list of nodes for the graph. If the list contains non-`TNode` objects, they will be converted to `TNode` objects using `TGraphFactory.create_node`.
    edges : list[tuple[int, Any]] | list[TEdge]
        The list of edges for the graph. If the list contains non-`TEdge` objects, they will be converted to `TEdge` objects using `TGraphFactory.create_edge`.
    
    Returns
    -------
    TGraph
        The new `TGraph` object.
    """
    G : TGraph = TGraphBuilder.create_graph(nodes, edges);
    return G;

def get_adjacency_list(nodes: list[Any] | list[TNode] | TGraph, edges: list[tuple[int, Any]] | list[TEdge]) -> AdjacencyList:
    """
    Creates an adjacency list from the given nodes and edges.
    
    Parameters
    ----------
    nodes : list[Any] | list[TNode] | TGraph
        The list of nodes for the graph. If the list contains non-`TNode` objects, they will be converted to `TNode` objects using `TGraphFactory.create_node`.
    edges : list[tuple[int, Any]] | list[TEdge]
        The list of edges for the graph. If the list contains non-`TEdge` objects, they will be converted to `TEdge` objects using `TGraphFactory.create_edge`.
    
    Returns
    -------
    AdjacencyList
        The adjacency list of the graph.
    """
    if isinstance(nodes, TGraph):
        nodes = nodes.nodes;
        edges = nodes.edges;
    return TGraphBuilder.create_adjacency_list(nodes, edges);

def get_adjacency_matrix(nodes: list[Any] | list[TNode] | TGraph, edges: list[tuple[int, Any]] | list[TEdge]) -> AdjacencyMatrix:
    """
    Creates an adjacency matrix from the given nodes and edges.
    
    Parameters
    ----------
    nodes : list[Any] | list[TNode]
        The list of nodes for the graph. If the list contains non-`TNode` objects, they will be converted to `TNode` objects using `TGraphFactory.create_node`.
    edges : list[tuple[int, Any]] | list[TEdge]
        The list of edges for the graph. If the list contains non-`TEdge` objects, they will be converted to `TEdge` objects using `TGraphFactory.create_edge`.
    
    Returns
    -------
    AdjacencyMatrix
        The adjacency matrix of the graph.
    """
    if isinstance(nodes, TGraph):
        nodes = nodes.nodes;
        edges = nodes.edges;
    return TGraphBuilder.create_adjacency_matrix(nodes, edges);