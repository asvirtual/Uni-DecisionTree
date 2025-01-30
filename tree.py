from node import Node
from data import Data
import numpy as np


'''
    Represents a decision tree
    @param root: the root node of the tree, shape of class Node
'''
class Tree:
    def __init__(self, root=None):
        self.__root = root

    
    '''
        Returns the final decision made by the tree
        @param query: the query to be answered, shape of class Query
    '''
    def decide(self, query):
        try:
            return self.__root.decide(query)
        except ValueError as e:
            print(e)
            return None
        
    
    def get_root(self):
        return self.__root
    

    def print_tree(self, node=None, level=0):
        if node is None: node = self.__root

        print("  " * level + str(node))

        for value, output in node.get_decisions().items():
            print("  " * (level + 1) + f"{value} -> {output}")

        for value, child in node.get_children().items():
            print("  " * (level + 1) + f"{value}: ")
            self.print_tree(child, level + 2)
        
            
    '''
        Returns the best category to split the data
        @param data: the data to be split, shape of class Data
        @param categories: the categories to be considered for the split, shape of list of class Category
    '''
    def get_best_category(data, categories):
        def calculate_entropy(probabilities):
            if probabilities.count(1.0) > 0: return 0

            result = 0
            for q in probabilities:
                if q == 0: continue # Avoid log(0)
                result -= q * np.log2(q)

            return result

        best_category = categories[0]
        best_category_gain = 0

        # Calculate the number of samples for each possible output among all data entries associated with the parent node's category
        decisions = data.get_decisions()
        total_outputs = {}
        for output in data.get_outputs():
            total_outputs[output] = decisions.count(output)

        # Iterate over all categories to find the one with the highest gain
        for category in categories:
            # Split the entries into subsets based on the values of the current category
            subsets = []
            for value in category.get_values():
                subsets.append(data.get_subset(category, value))

            # Calculate the remainder (conditional entropy) of the current category
            remainder = 0
            for subset in subsets:
                if len(subset) == 0: continue

                # Calculate the number of samples for each possible output among all data entries associated with the current category
                category_outputs = {}
                for output in subset.get_outputs():
                    category_outputs[output] = subset.get_decisions().count(output)

                # Compute the conditional entropy of the current category based on the output distribution of the subset
                # H(category) = sum( (|subset| / |total_set|) * (-P(output) * log2(P(output))) ) for all categories' subsets
                remainder += len(subset) / len(decisions) * calculate_entropy([ category_outputs[output] / len(subset) for output in category_outputs ])
            
            # Calculate the gain of the current category
            # Gain = H(parent) - Remainder
            gain = 0
            if len(decisions) > 0: gain = calculate_entropy([ total_outputs[output] / len(decisions) for output in total_outputs ]) - remainder

            if gain > best_category_gain:
                best_category = category
                best_category_gain = gain

        return best_category
            

    def build(training_data, categories):
        if categories is None or len(categories) == 0:
            return None
        
        # Find the best category to split the data
        best_category = Tree.get_best_category(training_data, categories)
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
                    # If we never exited from the loop with a break statement (i.e. all decisions are the same), add a decision to the node
                    node.add_decision(value, candidate_output)
                    break
            else:
                # If we never exited from the loop with a break statement, there is no obvious decision, 
                # so we need to further split the data based on one of the remaining categories and
                # create a child node for the value by recursively calling the function
                node.add_child(
                    value,
                    Tree.build(
                        subset,
                        list(filter(lambda c: c != best_category, categories))
                    )
                )

        return node

            