"""
Class definitions for primitive node structures and trees

@author nrdc
@version 1.0
@date 2024-12-14
"""
from typing import Any, List;
import random;


class Node:
    __slots__ = ['value', 'father', 'children', ];
    
    def __init__(self, value: Any, father: "Node" = None, children: List["Node"] = None):
        """
        Instantiates a new `Node` object with the given value, father, and children.
        
        Parameters
        ----------
        value : Any
            The value of the node.
        father : Node
            The father of the node.
        children : List[Node]
            The children of the node.
            
        Returns
        -------
        None
        """
        self.value = value;
        self.father = father;
        self.children = children;
        
        if self.children is not None:
            for child in self.children:
                if child.father != self:
                    child.father = self;
                    
    def __str__(self) -> str:
        return f"Node[value=\"{self.value}\", father?=\"{self.father}\", children?=\"{self.children}\"]";
    
    def __repr__(self):
        return self.__str__();
    
    def __eq__(self, other: "Node") -> bool:
        try:
            return self.value == other.value and self.father == other.father and self.children == other.children;
        except AttributeError:
            return False;
    
    def __hash__(self) -> int:
        return hash(self.value);
    
    @staticmethod
    def randomNode(value_type: type = None) -> "Node":
        """
        Instantiates a new `Node` object with a random value of the given type.
        
        Parameters
        ----------
        value_type : type
            The type of the value of the node.
            
        Returns
        -------
        Node
            A new `Node` object with a random value of the given type.
        """
        if value_type == int:
            return Node(random.randint(-100, 100));
        elif value_type == float:
            return Node(random.uniform(-100, 100));
        elif value_type == str:
            return Node(random.choice(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']));
        else:
            return Node(None);
