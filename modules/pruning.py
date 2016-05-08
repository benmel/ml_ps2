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

    if root.label != None:
        return
    elif (True in map(lambda x: x.label == None, root.children.values()):
        unpruned = validation_accuracy(root, validation_set)
        children = root.children
        root.label = mode(training_set)
        root.children = {}
        pruned = validation_accuracy(root, validation_set)
        if pruned >= unpruned:
            root.children = {}
            return root
        else:
            root.label = None
            root.children = children
            return root
    elif root.is_nominal:
        matching = split_on_nominal(training_set, root.decision_attribute)
        matching_v = split_on_nominal(validation_set, root.decision_attribute)
        for k in matching.keys():
            root.children[k] = reduced_error_pruning(root.children[k], matching[k], matching_v[k])
    else:
        matching = split_on_numerical(training_set, root.decision_attribute, root.splitting_value)
        matching_v = split_on_numerical(validation_set, root.decision_attribute, root.splitting_value)
        root.children[0] = reduced_error_pruning(root.children[0], matching[0], matching_v[0])
        root.children[1] = reduced_error_pruning(root.children[1], matching[1], matching_v[1])
# 

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