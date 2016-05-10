import os.path
from operator import xor
from parse import *
from datetime import datetime

# DOCUMENTATION
# ========================================
# this function outputs predictions for a given data set.
# NOTE this function is provided only for reference.
# You will not be graded on the details of this function, so you can change the interface if 
# you choose, or not complete this function at all if you want to use a different method for
# generating predictions.

def create_predictions(tree, predict):
    '''
    Given a tree and a url to a data_set. Create a csv with a prediction for each result
    using the classify method in node class.
    '''
    filename = 'results' + str(datetime.now()) + '.csv'
    with open(filename, 'w') as f:
      (array, attributes) = parse(predict, True)
      for i in xrange(len(array)):
        array[i][0] = tree.classify(array[i])
        for j in xrange(len(array[i])):
          array[i][j] = '?' if array[i][j] is None else array[i][j]
          f.write(str(array[i][j]) + ',')
        f.write('\n')  
