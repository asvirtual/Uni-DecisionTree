from category import Category
from data import Query


'''
    Represents a node in the decision tree
    @param category: the category of the node, shape of class Category
    @param children: the children of the node, shape of dict of {value: node} where value is one of the values of the category 
        and node is the associated child node
    @param decisions: the decisions of the node, shape of dict of {value: decision}, where decision is a boolean value.
        True means the decision is positive, False means the decision is negative, and None means the decision is not yet made.
'''
class Node:
    def __init__(self, category, decisions=None):
        if not isinstance(category, Category):
            raise ValueError(f"[ERROR] Category must be of type Category, got {type(category)}")
        
        self.__category = category
        self.__decisions = decisions if decisions is not None else {}
        self.__children = {}


    def __str__(self):
        return f"Node: {self.__category}"
    

    def get_category(self):
        return self.__category
    

    def get_decisions(self):
        return self.__decisions
    

    def get_children(self):
        return self.__children
    

    def add_decision(self, value, decision):        
        self.__decisions[value] = decision
    

    def decide(self, query):
        if not isinstance(query, Query):
            raise ValueError(f"[ERROR] Query must be of type Query, got {type(query)}")
        
        category_value = query[self.__category]
        decision = self.__decisions.get(category_value)
        if decision is not None:
            return decision
        
        child = self.__children[category_value]
        return child.decide(query)
    

    def add_child(self, value, child):
        if value is None or child is None:
            return
        
        if not isinstance(child, Node):
            raise ValueError(f"[ERROR] Child must be of type Node, got {type(child)}")
        
        if value not in self.__category:
            raise ValueError(f"[ERROR] Value {value} not valid for category {self.__category}")
        
        self.__children[value] = child
