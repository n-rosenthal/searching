import src.datastructures.queues as Queues;

def depthFirstSearch(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if start not in graph:
        return None
    for node in graph[start]:
        if node not in path:
            newpath = depthFirstSearch(graph, node, end, path)
            if newpath: return newpath
    return None