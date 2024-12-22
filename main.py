from typing import Set, List;
from src.datastructures.CommonNodes import BasicEdge, BasicGraph, BasicNode;
from src.datastructures.primitives.NodicVisualizers import visualize, visualize_tree;
from src.datastructures.NodicWays import Walk, Trail, Path, is_path
from src.operators.ElementarNodicOperators import MEdge, Multigraph;

def main():
    A, B, C, D, E, F    = BasicNode("A"), BasicNode("B"), BasicNode("C"), BasicNode("D"), BasicNode("E"), BasicNode("F");
    g                   = Multigraph.from_nodes({A, B, C, D, E, F}, {BasicEdge(A, B), BasicEdge(B, C), BasicEdge(C, A), 
                                                               BasicEdge(C, D), BasicEdge(D, E), BasicEdge(E, C),
                                                               BasicEdge(E, F)});
    
    G, H, I, J, K, L   = BasicNode("G"), BasicNode("H"), BasicNode("I"), BasicNode("J"), BasicNode("K"), BasicNode("L");
    h                  = Multigraph.from_nodes({G, H, I, J, K, L}, {BasicEdge(G, H), BasicEdge(H, I), BasicEdge(I, J), 
                                                               BasicEdge(J, K), BasicEdge(K, L), BasicEdge(L, G)});
    
    #   Add a new node to the graph
    print(g.nodes);
    g += G;
    print(g.nodes);
    
    
    return;

if __name__ == "__main__": main();