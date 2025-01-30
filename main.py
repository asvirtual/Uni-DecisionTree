from tree import Tree, learn_decision_tree
from data import load_json


categories, training_data, query = load_json("data.json")
tree = Tree(learn_decision_tree(training_data, categories))
tree.print_tree(tree.root, 0)
print(tree.decide(query))