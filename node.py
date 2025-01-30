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
        
        self.category = category
        self.decisions = decisions if decisions is not None else {}
        self.children = {}


    def __str__(self):
        return f"Node: {self.category.get_name()}"
    

    def get_category(self):
        return self.category
    

    def get_children(self):
        return self.children
    

    def add_decision(self, value, decision):        
        self.decisions[value] = decision
    

    def decide(self, query):
        if not isinstance(query, Query):
            raise ValueError(f"[ERROR] Query must be of type Query, got {type(query)}")
        
        category_value = query.get(self.category)
        decision = self.decisions.get(category_value)
        if decision is not None:
            return decision
        
        child = self.children.get(category_value)        
        return child.decide(query)
    

    def add_child(self, value, child):
        if value is None or child is None:
            return
        
        if not isinstance(child, Node):
            raise ValueError(f"[ERROR] Child must be of type Node, got {type(child)}")
        
        if value not in self.category.get_values():
            raise ValueError(f"[ERROR] Value {value} not valid for category {self.category}")
        
        self.children[value] = child
