"""
Functions for visualizing Graph structures.

@author nrdc
@since 1.1
@date 2024-12-20
"""

from src.datastructures.primitives.NodicBasis import INode, IEdge, IGraph;
import matplotlib.pyplot as plt;
import networkx as nx;
import pydot;
from networkx.drawing.nx_pydot import write_dot, graphviz_layout

def visualize(graph: IGraph) -> None:
    G = nx.Graph();
    for node in graph.nodes:
        G.add_node(node.value);
    for edge in graph.edges:
        G.add_edge(edge.source.value, edge.target.value);
    pos = nx.spring_layout(G);
    nx.draw(G, pos, with_labels=True);
    plt.show();
    
    return;

def visualize_tree(tree: IGraph) -> None:
    G = nx.Graph();
    for node in tree.nodes:
        G.add_node(node.value);
    for edge in tree.edges:
        G.add_edge(edge.source.value, edge.target.value);
    pos = graphviz_layout(G, prog="twopi");
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=200, width=2);
    plt.show();
    return;