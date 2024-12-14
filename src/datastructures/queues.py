"""
Implementations of queue data structures.

@author nrdc
@version 1.0
@date 2024-12-14
"""

from src.datastructures.primitives.nodes import Node;
from typing import Any, List, Set;


class Queue:
    """A simple implementation of a queue data structure over `Node` objects.
    A queue is a FIFO (first-in, first-out) data structure.
    """
    
    def __init__(self):
        """
        Instantiates a new empty `Queue` object.
        """
        self._head : Node = None;
        self._tail : Node = None;
        self._size : int = 0;
        self._nodes : Set[Node] = set();
        
    def enqueue(self, value: Any) -> None:
        """
        Enqueues a value at the end of the queue.
        
        Parameters
        ----------
        value : Any
            The value to enqueue.
        """
        new_node = Node(value);
        if self._head is None:
            self._head = new_node;
            self._tail = new_node;
        else:
            if(self._tail.children is None):
                self._tail.children = [];
            self._tail.children.append(new_node);
            self._tail = new_node;
        self._nodes.add(new_node);
        self._size += 1;
        
    def dequeue(self) -> Any:
        """
        Dequeues the value at the beginning of the queue.
        
        Returns
        -------
        Any
            The value dequeued.
        """
        if self._head is None or self._size == 0 or self._head.children is None:
            raise IndexError("Queue is empty.");
        value = self._head.value;
        self._head = self._head.children[0];
        self._nodes.remove(self._head);
        self._size -= 1;
        return value;
    
    def size(self) -> int:
        """
        Returns the size of the queue.
        
        Returns
        -------
        int
            The size of the queue.
        """
        return self._size;
    
    def __str__(self) -> str:
        return f"Queue[size={self._size}, head=\"{self._head}\", tail=\"{self._tail}\"]";
    
    def __repr__(self):
        return self.__str__();
    
    def __eq__(self, other: "Queue") -> bool:
        return self._head == other._head and self._tail == other._tail and self._size == other._size;
    
    def __hash__(self) -> int:
        return hash((self._head, self._tail, self._size));
    
    def __len__(self) -> int:
        return self.size();


