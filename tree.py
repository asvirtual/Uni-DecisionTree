from node import Node
from data import Data
import numpy as np


class Tree:
    def __init__(self, root=None):
        self.root = root

    
    '''
        Returns the final decision made by the tree
        @param data: the data to be used to make the decision, shape of class Data
    '''
    def decide(self, data):
        try:
            return self.root.decide(data)
        except ValueError as e:
            print(e)
            return None
        
    
    def get_root(self):
        return self.root
    

    def print_tree(self, node, level):
        if node is not None:
            print("  " * level + str(node.category.get_name()))
            for value, child in node.children.items():
                print("  " * (level + 1) + f"{value}:")
                self.print_tree(child, level + 2)
        
        

def get_best_category(data, categories):
    def calculate_entropy(probabilities):
        if probabilities.count(1.0) > 0: return 0

        result = 0
        for q in probabilities:
            if q == 0: continue
            result -= q * np.log2(q)

        return result

    best_category = categories[0]
    best_category_gain = 0

    # Calculate the number of positive and negative samples among all entries of the parent node
    decisions = data.get_decisions()
    total_outputs = {}
    for output in data.get_outputs():
        total_outputs[output] = decisions.count(output)

    for category in categories:
        # Split the entries into subsets based on the values of the current category
        subsets = []
        for value in category.get_values():
            subsets.append(data.get_subset(category, value))

        # Calculate the remainder of the current category
        remainder = 0
        for subset in subsets:
            if len(subset.get_decisions()) == 0: continue

            category_outputs = {}
            for output in subset.get_outputs():
                category_outputs[output] = subset.get_decisions().count(output)

            remainder += len(subset.get_decisions()) / len(decisions) * calculate_entropy([ category_outputs[output] / len(subset.get_decisions()) for output in category_outputs ])
        
        # Calculate the gain of the current category
        gain = 0
        if len(decisions) > 0: gain = calculate_entropy([ total_outputs[output] / len(decisions) for output in total_outputs ]) - remainder

        if gain > best_category_gain:
            best_category = category
            best_category_gain = gain

    return best_category
        

def learn_decision_tree(training_data, categories):
    if categories is None or len(categories) == 0:
        return None
    
    # Find the best category to split the data
    best_category = get_best_category(training_data, categories)
    node = Node(best_category)


    # Split the data into subsets based on the values of the best category
    for value in best_category.get_values():
        subset = training_data.get_subset(best_category, value)

        # If all entries in the subset have the same decision, add a decision to the node
        for candidate_output in subset.get_outputs():
            # For each possible output in the subset, check if every entry of the subset has the same decision as output
            for entry in subset.get_data():
                # When an entry with a different decision from the candidate output is found, break the loop
                if candidate_output != entry.get_decision():
                    break
            else:
                # If the loop never terminated (i.e. all decisions are the same), add a decision to the node
                node.add_decision(value, candidate_output)
                break
        else:
            # If the loop terminated, there is no obvious decision, so we need to differentiate by another category
            filtered_categories = []
            for c in categories:
                if c != best_category: filtered_categories.append(c)

            # If entries of the subset have different decisions, create a child node for the value and learn the decision tree recursively
            node.add_child(
                value,
                learn_decision_tree(
                    subset,
                    filtered_categories
                )
            )

    return node

        