from primitives.datatypes.TNode import TNode, TEdge, AdjacencyList, AdjacencyMatrix, getAdjacencyList, getAdjacencyMatrix;

class TGraph:
    nodes: set[TNode] = set();
    edges: set[TEdge] = set();

    def __init__(self, nodes: set[TNode] = set(), edges: set[TEdge] = set()) -> None:
        """
        Initializes a TGraph object with the given nodes and edges.
        
        Parameters:
        ----------
        nodes : set[TNode], optional
            The nodes of the graph. Defaults to an empty set.
        edges : set[TEdge], optional
            The edges of the graph. Defaults to an empty set.
        """
        self.nodes = nodes;
        self.edges = edges;
        return;
    
    def adjacencyList(self) -> AdjacencyList:
        """
        Gets the adjacency list of the graph.
        
        Returns
        -------
        AdjacencyList
            The adjacency list of the graph.
        """
        return getAdjacencyList(self.edges);
    
    def adjacencyMatrix(self) -> AdjacencyMatrix:
        """
        Gets the adjacency matrix of the graph.
        
        Returns
        -------
        AdjacencyMatrix
            The adjacency matrix of the graph.
        """
        return getAdjacencyMatrix(self.edges);
    
