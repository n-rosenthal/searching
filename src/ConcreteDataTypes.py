from    primitives.TGraphBuilder    import build_graph, create_node, create_edge;
from    primitives.datatypes.TGraph import TGraph, TNode, TEdge;
from    GraphUtils                  import ascii_nodes;
from    functionals.GraphProtocols  import Sizeable, Parentable, UnionAssociative;
from    typing import Any, TypeVar

__version__ = "1.0.0";
__author__ = "nrdc";
__status__ = "Development";
__import__ = "src.ConcreteDataTypes";

#   Associative Graphs
class UAGraph(TGraph):
    """
    `UAGraph` is a `TGraph` graph that implements the `UnionAssociative` protocol.
    """
    def __init__(self, nodes: set[TNode] = set(), edges: set[TEdge] = set()) -> None:
        super().__init__(nodes, edges);
        return;
    
    def __add__(self, other: "UAGraph") -> "UAGraph":
        """
        The `+` operator between two `UAGraph` graphs implements the
        `UnionAssociative` protocol, which means that given two graphs, G1 and G2,
        we have that G3 = G1 + G2 = G2 + G1.
        
        Parameters
        ----------
        other : UAGraph
            The other graph to add to this graph.
        
        Returns
        -------
        UAGraph
            The result of adding this graph to the other graph.
        
        Notes
        -----
        The `+` operator is associative, meaning that G1 + (G2 + G3) = (G1 + G2) + G3 = G1 + (G3 + G2),
        for all G1, G2, G3 of type `UAGraph`.
        """
        ascii_letters = ascii_nodes(len(self.nodes) + len(other.nodes));
        nodes : set[TNode] = self.nodes + other.nodes;
        edges : set[TEdge] = self.edges + other.edges;
        
        for i in range(1, len(nodes) + 1):
            nodes[i-1].value = ascii_letters[i - 1].value;
            nodes[i-1].id = i;
        
        return UAGraph(nodes, edges);
    
    def __or__(self, other: "UAGraph") -> "UAGraph":
        return self.__add__(other);
#   Identifiers for interesting graphs
##  Empty Graph
EmptyGraph  :   TGraph = build_graph(
                    nodes = [],
                    edges = []
                );

##  Complete Graphs Kn
def Kn(n: int) -> TGraph:
    """
    Returns a complete graph of size n, Kn.
    
    Parameters
    ----------
    n : int
        The size of the complete graph.
        
    Raises
    ------
    ValueError
        If n < 0
        
    NotImplemented
        If n > 26
    
    Returns
    -------
    TGraph
        The complete graph of size n.
    """
    if n < 0:
        raise ValueError("n must be greater than 0");
    if n > 26:
        raise NotImplemented("n must be less than 26");
    
    nodes : list[TNode] = ascii_nodes(n);
    edges : list[TEdge] = [];
    
    for i in range(n):
        for j in range(i + 1, n):
            edges.append((nodes[i], nodes[j]));
    
    return build_graph(nodes, edges);




PNode = TypeVar("PNode", bound="PNode");
class PNode(TNode, Parentable, Sizeable):
    """
    `PNode` is a `TNode` graph node that implements the `Parentable` and `Sizeable` protocols. 
    The `Sizeable` protocol implies that PNode has (1) a `neighbors` field of type `list[PNode]` and (2) a method `degree()` that returns the degree of the node (`= len(neighbors)`).
    The `Parentable` protocol implies that PNode has a `parent` field of type `TNode`.
    
    Attributes
    ----------
    neighbors  : list[PNode]
        The neighbors of the node.
    parent  : TNode
        The parent node of the node.
    value   : str | int
        The value of the node.
    id      : int
        The id of the node.
        
    Methods
    -------
    degree() -> int
        Returns the degree of the node.
        
    parent() -> TNode
        Returns the parent node of the node.
    """
    def __init__(self,  value: int | str,
                        node_id: int, 
                        parent: PNode | None = None,
                        neighbors: list["PNode"] = []) -> None:
        """
        Constructor for PNode.
        
        Parameters
        ----------
        value       (str | int):    The value of the node.
        node_id     (int):          The id of the node.
        parent      (PNode | None): The parent node of the node. Defaults to None.
        
        Raises
        ------
        NotImplementedError
            If the parent is not of type Node.
        """
        super().__init__(value, node_id);
        if parent is not None and not isinstance(parent, PNode):
            raise NotImplementedError("Node parent must be of type Node. Got: " + str(type(parent)));        
        self.parent = parent;
        
        for node in neighbors:
            if not isinstance(node, PNode):
                raise NotImplementedError("Node neighbors must be of type Node. Got: " + str(type(node)));
        self.neighbors = neighbors;
        
        
    def degree(self) -> int:
        """
        Returns the degree of the node.
        
        Returns
        -------
        int
            The degree of the node.
        """
        return len(self.neighbors);

def cast(graph: TGraph) -> UAGraph:
    return UAGraph(graph.nodes, graph.edges);
   
if __name__ == "__main__":
    K3, K4 = Kn(3), Kn(4);
    K3, K4 = cast(K3), cast(K4);
    K7 = K3 + K4;
    
    print(K7.nodes);
    print(K7.edges);
    