""" search_algorithms/src/primitives/Node.py 
The `Node.py` module defines the `Node`, `Edge` and `Graph` classes.

Classes:
    Node    : A node in a graph.
    Edge    : An edge in a graph.
    Graph   : A graph.
"""

import typing


#   Edge    type
type Edge = tuple[TNode, TNode];
"""
The `Edge` type represents an edge in a graph.
It is a tuple of two nodes.
"""

class TNode:
    """
    `TNode` is the type class for implementing nodes.
    
    Attributes:
        value       (int | str):    The value of the node.
        id          (int):          An identifier for the node. Defaults to None.
                                        The identifier is used to identify the node in a graph and it's not used by the node itself.
        parent      (TNode | None): The parent node of the node. Defaults to None.
    """
    def __init__(self,  value : str | int,
                        id : int | None = None,
                        parent = None) -> None:
        """
        Constructor for Node.
        
        Parameters
        ----------
        value       (int | str):    The value of the node.
        id          (int | None):   An identifier for the node. Defaults to None.
        
        Raises
        ------
        NotImplementedError
            If the value is not of type int or str, or if the id is not of type int.
        """
        if isinstance(value, int) or isinstance(value, str):
            self.value = value;
        else:
            raise NotImplementedError("Node value must be of type int or str. Got: " + str(type(value)));

        if id is not None and not isinstance(id, int):
            raise NotImplementedError("Node id must be of type int. Got: " + str(type(id)));
        self.id = id;
        
        if parent is not None and not isinstance(parent, TNode):
            raise NotImplementedError("Node parent must be of type Node. Got: " + str(type(parent)));
        self.parent = parent;
        
    def __str__(self) -> str:
        """
        Returns a string representation of the Node object, displaying its id and value.

        Returns
        -------
        str
            A string in the format '[(#id) value]', where 'id' is the identifier of the node
            and 'value' is the value of the node.
        """
        return f"[(#{self.id}) {self.value}]";
    
    def __repr__(self) -> str:
        """
        Returns a string representation of the Node object, displaying its id and value.
        
        Returns
        -------
        str
            A string in the format '[(#id) value]', where 'id' is the identifier of the node
            and 'value' is the value of the node.
        """
        return self.__str__();
    
    def __hash__(self) -> int:
        """
        Returns the hash value of the Node object, which is the hash of the node's value.
        
        Returns
        -------
        int
            The hash value of the Node object.
        """
        return hash(self.value);
    
    def __eq__(self, other: "TNode") -> bool:
        """
        Checks if the given node is equal to the current node.
        
        Equality is determined by comparing the values of the nodes.
        
        Parameters
        ----------
        other : TNode
            The node to compare with.
            
        Raises
        ------
        TypeError
            If the `other` parameter is not of type Node.
        
        Returns
        -------
        bool
            True if the nodes are equal, False otherwise.
        """
        if not isinstance(other, TNode):
            raise TypeError("other must be of type Node");
        return self.value == other.value;
    
#   Edge    type
type TEdge = set[TNode, TNode];
"""
`TEdge` is the type for representing an edge in a graph.
An edge is a set of two nodes.
"""

type AdjacencyList = dict[TNode, list[TNode]];
"""
The `AdjacencyList` type represents an adjacency list for a graph.
It is a dictionary where the keys are nodes and the values are lists of nodes that are adjacent to the key node.
Two nodes are adjacent if they are connected by an edge in the graph.
"""

type AdjacencyMatrix = list[list[int]];
"""
The `AdjacencyMatrix` type represents an adjacency matrix for a graph.
It is a list of lists where the rows and columns are nodes and the values are 1 if the nodes are adjacent and 0 otherwise.
"""

def edge(v: TNode, w: TNode) -> TEdge:
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
        The edge between v and w.
    """
    return {v, w};

def getNodesFromEdges(edges: list[TEdge]) -> list[TNode]:
    """
    Returns a list of nodes from a list of edges.
    
    Parameters
    ----------
    edges : list[TEdge]
        The list of edges to get the nodes from.
    
    Returns
    -------
    list[TNode]
        The list of nodes.
    """
    nodes : set[TNode] = set();
    for edge in edges:
        u, v = tuple(edge);
        nodes.add(u);
        nodes.add(v);
    return list(nodes);

def getAdjacencyList(edges: list[TEdge]) -> AdjacencyList:
    """
    Creates an adjacency list from a list of edges.
    
    Parameters
    ----------
    edges : list[TEdge]
        The list of edges to create the adjacency list from.
    
    Returns
    -------
    AdjacencyList
        The adjacency list.
    """
    nodes : list[TNode] = getNodesFromEdges(edges);
    adjacencyList : AdjacencyList = {node: [] for node in nodes};
    for edge in edges:
        u, v = tuple(edge);
        
        if u == v:
            continue;
        
        if u not in adjacencyList[v]:
            adjacencyList[v].append(u);
        if v not in adjacencyList[u]:
            adjacencyList[u].append(v);
    return adjacencyList;


            
def lexsort(nodes):
    nodes : list[TNode] = list(nodes);
    nodes.sort(key=lambda node: node.value);
    return nodes;

def pretty_print_adjacency_list(adjacencyList: AdjacencyList, ignore_id: bool = False) -> None:
    """
    Prints the adjacency list in a pretty format.
    
    Parameters
    ----------
    adjacencyList : AdjacencyList
        The adjacency list to print.
    ignore_id : bool, optional
        If True, the node id will not be printed. Defaults to False.
    """
    nodes : list[TNode] = list(adjacencyList.keys());
    for node in nodes:
        if ignore_id:
            print(f"{node.value}: {adjacencyList[node]}");
        else:
            print(f"{node}: {adjacencyList[node]}");

def getAdjacencyMatrix(edges: list[TEdge]) -> AdjacencyMatrix:
    """
    Creates an adjacency matrix from a list of edges.
    
    Parameters
    ----------
    edges : list[TEdge]
        The list of edges to create the adjacency matrix from.
    
    Returns
    -------
    AdjacencyMatrix
        The adjacency matrix.
    """
    nodes : list[TNode] = getNodesFromEdges(edges);
    adjacencyMatrix : AdjacencyMatrix = [[0 for _ in range(len(nodes))] for _ in range(len(nodes))];
    for edge in edges:
        u, v = tuple(edge);
        adjacencyMatrix[nodes.index(u)][nodes.index(v)] = 1;
        adjacencyMatrix[nodes.index(v)][nodes.index(u)] = 1;
    return adjacencyMatrix;
    
        
def pretty_print_adjacency_matrix(adjacencyMatrix: AdjacencyMatrix) -> None:
    """
    Prints the adjacency matrix in a pretty format.
    
    Parameters
    ----------
    adjacencyMatrix : AdjacencyMatrix
        The adjacency matrix to print.
    """
    for row in adjacencyMatrix:
        print(row);

