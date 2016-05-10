from random import shuffle
from ID3 import *
from operator import xor
from parse import parse
import matplotlib.pyplot as plt
import os.path
from pruning import validation_accuracy
from pruning import reduced_error_pruning
from random import sample
from numpy import arange

# NOTE: these functions are just for your reference, you will NOT be graded on their output
# so you can feel free to implement them as you choose, or not implement them at all if you want
# to use an entirely different method for graphing

def get_graph_accuracy_partial(train_set, attribute_metadata, validate_set, numerical_splits_count, depth, pct, prune):
    '''
    get_graph_accuracy_partial - Given a training set, attribute metadata, validation set, numerical splits count, and percentage,
    this function will return the validation accuracy of a specified (percentage) portion of the trainging setself.
    '''
    sample_size = int(pct*len(train_set))
    sample_set = sample(train_set, sample_size)
    tree = ID3(sample_set, attribute_metadata, numerical_splits_count, depth)
    if prune:
        reduced_error_pruning(tree, train_set, validate_set)
    return validation_accuracy(tree, validate_set)


def get_graph_data(train_set, attribute_metadata, validate_set, numerical_splits_count, depth, iterations, pcts, prune):
    '''
    Given a training set, attribute metadata, validation set, numerical splits count, iterations, and percentages,
    this function will return an array of the averaged graph accuracy partials based off the number of iterations.
    '''
    results = []
    for pct in pcts:
        partial = 0
        for x in range(iterations):
            partial += get_graph_accuracy_partial(train_set, attribute_metadata, validate_set, numerical_splits_count, depth, pct, prune)
        average = partial/iterations
        results.append(average)
    return results        


# get_graph will plot the points of the results from get_graph_data and return a graph
def get_graph(train_set, attribute_metadata, validate_set, numerical_splits_count, depth, iterations, lower, upper, increment):
    '''
    get_graph - Given a training set, attribute metadata, validation set, numerical splits count, depth, iterations, lower(range),
    upper(range), and increment, this function will graph the results from get_graph_data in reference to the drange
    percentages of the data.
    '''
    pcts = arange(lower, upper, increment)
    data_pruned = get_graph_data(train_set, attribute_metadata, validate_set, numerical_splits_count, depth, iterations, pcts, True)
    data_unpruned = get_graph_data(train_set, attribute_metadata, validate_set, numerical_splits_count, depth, iterations, pcts, False)
    plt.plot(pcts, data_pruned, label="Pruned")
    plt.plot(pcts, data_unpruned, label="Unpruned")
    plt.legend(loc='lower right')
    plt.savefig('test.png')
    