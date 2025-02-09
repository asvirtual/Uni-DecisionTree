from tree import Tree
from data import load_json


categories, training_data, query = load_json("data.json")
tree = Tree(Tree.build(training_data, categories))

print("Built the following DecisionTree:\n")
tree.print_tree()

print(f"\nPredicted output for query: {query}")
print(f" -> {tree.decide(query)}")

