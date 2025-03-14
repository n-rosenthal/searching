""" search_algorithms/src/primitives/Node.py 
The `Node.py` module defines the `Node`, `Edge` and `Graph` classes.

Classes:
    Node    : A node in a graph.
    Edge    : An edge in a graph.
    Graph   : A graph.
"""

from typing import Any;


#   Edge    type
type Edge = tuple[Node, Node];
"""
The `Edge` type represents an edge in a graph.
It is a tuple of two nodes.
"""

def edge(v: "Node", w: "Node") -> Edge:
    """
    Creates an edge between two nodes."""

class Node:
    """
    `Node` represents a node in a graph.
    
    Attributes:
        attributes  (set): A set of attributes associated with the node. Defaults to the empty set.
        value       (Any): The value of the node. Defaults to None.
        node_id     (int): An identifier for the node. Defaults to None.
        neighbors   (set): A set of nodes that are connected to the current node.
    """

    def __init__(self, value : Any, node_id : int | None = None, attributes : set | None = None, neighbors : set | None = None):
        """
        Constructor for Node.
        
        Parameters:
            value       (Any)      : The value of the node.
            node_id     (int)      : An identifier for the node. Defaults to None.
            attributes  (set)      : A set of attributes associated with the node. Defaults to the empty set.
            neighbors   (set)      : A set of nodes that are connected to the current node. Defaults to the empty set.
        """
        self.value = value
        self.node_id = node_id
        self.attributes = attributes or set()
        self.neighbors = neighbors or set()
    
    def __repr__(self):
        return f"Node(value={self.value}, node_id={self.node_id})";
        
    def __str__(self):
        return f"(#{self.node_id}, {self.value})";
    
    def __hash__(self):
        return hash((self.value, self.node_id));
    
    def __eq__(self, other):
        return self.value == other.value and self.node_id == other.node_id
    
    def __ne__(self, other):
        return not self == other;

class GraphStatus:
    """
    `GraphStatus` class is used for message exchange between functions and error handling.
    """
    def __init__(self, status : str, message : str | None = None, code : int | None = None):
        self.status = status;
        self.message = message;
        self.code = code;
    
GraphOperationSuccess   : GraphStatus = GraphStatus(status="SUCCESS", code=0);
GraphOperationFailure   : GraphStatus = GraphStatus(status="FAILURE", code=1);
NodeTypeError           : GraphStatus = GraphStatus(status="TYPE_ERROR", code=2);
EdgeTypeError           : GraphStatus = NodeTypeError;
GraphStatusException    : GraphStatus = GraphStatus(status="EXCEPTION", code=3);
GraphImpossibleOperation: GraphStatus = GraphStatus(status="IMPOSSIBLE_OPERATION", code=4);
GraphExit               : GraphStatus = GraphStatus(status="EXIT", code=5);

class Graph:
    """
    `Graph` represents a graph.
    The index is maintained if nodes are inserted; if values are inserted, the `self.index` is used.
    
    Attributes:
        nodes   (dict[int, Node]): A dictionary mapping node IDs to nodes.
        edges   (dict[Node, set[Node]]): A list of edges in the graph.
    """
    def __init__(self, nodes : dict[int, Node] | None = None, edges : list[tuple[Node, Node]] | None = None):
        """
        Constructor for Graph.
        
        Parameters:
            nodes   (dict[int, Node] | None): A dictionary mapping node IDs to nodes. Defaults to the empty dictionary.
            edges   (set[tuple[Node, Node]] | None): A set of edges in the graph. Defaults to the empty set.
        """
        #   Static type checking
        if nodes:
            assert isinstance(nodes, dict);
            assert isinstance(list(nodes.values())[0], Node);
        if edges:
            assert isinstance(edges, list);
            assert isinstance(list(edges)[0], tuple);
                
        self.nodes = nodes or {};
        self.edges : dict[Node, set[Node]] = {};
        
        #   Identification of the nodes in the graph
        if self.nodes:
            #   Accumulates a list of already used indices
            used_indices : set[int] = set();
            for node in self.nodes.values():
                if isinstance(node.node_id, int):
                    used_indices.add(node.node_id);
            #   Find the next available index
            self.index = max(used_indices) + 1 if used_indices else 0;
        else:
            self.index = 0;
            
        #   Set the node IDs of the nodes in the graph
        if self.nodes:
            for node in self.nodes.values():
                if node.node_id is None:
                    node.node_id = self.index;
                    self.index += 1;
        
        if edges:
            for edge in edges:
                v, w = edge;
                
                if v.value in self.nodes and w.value in self.nodes:
                    self.edges[v].insert(w);
                    self.edges[w].insert(v);
        
        
    def getNodes(self) -> set[Node]:
        """
        Returns a set of all nodes in the graph.
        
        Returns:
            set[Node]: A set of all nodes in the graph.
        """
        return set(self.nodes.values());
    
    def getNodesAsList(self) -> list[Node]:
        """
        Returns a list of all nodes in the graph, sorted by node ID.
        
        Returns:
            list[Node]: A list of all nodes in the graph, sorted by node ID.
        """
        V_g : list[Node] = list(self.getNodes());
        V_g.sort(key=lambda node : node.node_id);
        return V_g;
    
    def getEdges(self) -> set[tuple[Node, Node]]:
        """
        Returns a set of all edges in the graph.
        Accumulates a set of edges from each node's neighbors.
        
        Returns:
            set[tuple[Node, Node]]: A set of all edges in the graph.
        """
        edges : set[set[Node, Node]] = set();
        
        for node in self.nodes.values():
            for neighbor in node.neighbors:
                edges.add((node, neighbor));
        
        return edges;
    
    def getNode(self, node_id : int) -> Node:
        """Returns the Node with the given node_id
        
        Args:
            node_id (int): The node_id of the Node to return
        
        Raises:
            KeyError: If the node_id is not in the graph
        
        Returns:
            Node: The Node with the given node_id
        """
        try:
            return self.nodes[node_id];
        except KeyError:
            raise KeyError(f"Node with node_id {node_id} not found in graph");
    
    def setNode(self, node : Node):
        """Adds a node to the graph. If the node_id is None, assigns the next index.
        
        Args:
            node (Node): The node to add to the graph.
        
        Raises:
            KeyError: If the node_id is already in the graph.
        """
        if node.node_id is None:
            node.node_id = self.index;
            self.index += 1;
        else:
            #   Check if the node_id is already in the graph
            if node.node_id in self.nodes:
                raise KeyError(f"Node with node_id {node.node_id} already exists in graph");
            
        #   Add the node to the graph
        self.nodes[node.node_id] = node;
    
    def __repr__(self):
        return f"Graph(nodes={self.nodes}, edges={self.edges})";
    
    def __str__(self):
        return f"Graph(nodes={self.nodes}, edges={self.edges})";
    
#   Propose a neighborhood function
def neighborhood(node : Node, graph : Graph):
    if isinstance(node.value, int):
        neighbors : set[Node] = set();
        
        ln, rn = node.value - 1, node.value + 1;
        
        if ln in graph.nodes:
            neighbors.add(graph.nodes[ln]);
        if rn in graph.nodes:
            neighbors.add(graph.nodes[rn]);
        
        return neighbors;
    else:
        raise TypeError("Node value must be of type int");
    
if __name__ == "__main__":
    nodes : dict[int, Node] = {
        0 : Node(value=0), 1 : Node(value=1), 2 : Node(value=2), 3 : Node(value=3), 4 : Node(value=4), 5 : Node(value=5), 6 : Node(value=6), 7 : Node(value=7), 8 : Node(value=8), 9 : Node(value=9)
    };
    
    
    
    edges : list[Edge] = [
        (nodes[0], nodes[1]), (nodes[2], nodes[4]), (nodes[3], nodes[6]), (nodes[3], nodes[9])
    ];
    
    graph   : Graph = Graph(nodes=nodes, edges=edges);
    
    for node in graph.getNodesAsList():
        print(f"[{node}]: N({node.value}) = {node.neighbors}");
        
    #   getEdge
    print(graph.edges)
    print(graph.getEdge(graph.nodes[0], graph.nodes[1]));
        
        