#   Implementando a Classe `Graph`
##  Definições

Um grafo não-direcionado $G$ é uma tupla

$$G : (V[G], E[G])$$

Onde    $V[G]$ é o conjunto de vértices de $G$,
        $E[G]$ é o conjunto de arestas de $G$.

Uma aresta é um par não-ordenado de vértices $e = \{v, u\}, u,v \in V[G]$, isto é,

```Python
type Edge = set[Node, Node];
```




