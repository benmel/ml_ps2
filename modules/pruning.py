from node import Node
from ID3 import *
from operator import xor

# Note, these functions are provided for your reference.  You will not be graded on their behavior,
# so you can implement them as you choose or not implement them at all if you want to use a different
# architecture for pruning.

def reduced_error_pruning(root,training_set,validation_set):
    '''
    take the a node, training set, and validation set and returns the improved node.
    You can implement this as you choose, but the goal is to remove some nodes such that doing so improves validation accuracy.
    NOTE you will probably not need to use the training set for your pruning strategy, but it's passed as an argument in the starter code just in case.
    '''

    if root.label is not None or len(validation_set) == 0:
        return root

    node = Node()
    node.label = mode(validation_set)

    current_accuracy = validation_accuracy(root, validation_set)
    pruned_accuracy = validation_accuracy(node, validation_set)

    if current_accuracy < pruned_accuracy:
        return node
    
    if root.is_nominal:
        for key, value in root.children.items():
            matching = []
            for example in validation_set:
                if example[root.decision_attribute] == key:
                    matching.append(example)
            root.children[key] = reduced_error_pruning(value, training_set, matching)
    else:
        matching_less = []
        matching_greater_or_equal = []
        for example in validation_set:
            if example[root.decision_attribute] < root.splitting_value:
                matching_less.append(example)
            else:
                matching_greater_or_equal.append(example) 
        root.children[0] = reduced_error_pruning(root.children[0], training_set, matching_less)
        root.children[1] = reduced_error_pruning(root.children[1], training_set, matching_greater_or_equal)
   
    return root            

def validation_accuracy(tree,validation_set):
    '''
    takes a tree and a validation set and returns the accuracy of the set on the given tree
    '''
    outputs = 0
    total = 0
    for example in validation_set:
        outputs += 1.0 if tree.classify(example) == example[0] else 0
        total += 1.0
    return outputs / total

def countNodes(tree):
	nodes = 0
	if tree.label == None:
		for key in tree.children.keys():
			nodes += 1 + countNodes(tree.children[key])
		return nodes
	else:
		return 0