import math
from node import Node
import sys
import copy

def ID3(data_set, attribute_metadata, numerical_splits_count, depth):
    '''
    See Textbook for algorithm.
    Make sure to handle unknown values, some suggested approaches were
    given in lecture.
    ========================================================================================================
    Input:  A data_set, attribute_metadata, maximum number of splits to consider for numerical attributes,
	maximum depth to search to (depth = 0 indicates that this node should output a label)
    ========================================================================================================
    Output: The node representing the decision tree learned over the given data set
    ========================================================================================================

    '''
    attribute_modes_dict = attribute_modes(data_set, attribute_metadata)
    return ID3_recursive(data_set, attribute_metadata, numerical_splits_count, depth, attribute_modes_dict)

def ID3_recursive(data_set, attribute_metadata, numerical_splits_count, depth, attribute_modes_dict):
    if depth == 0 or check_homogenous(data_set) is not None or len(attribute_metadata) == 0:
        return default_node(data_set)    
    else:
        (best_attribute, split_value) = pick_best_attribute(data_set, attribute_metadata, numerical_splits_count)
        if best_attribute == False:
            return default_node(data_set)
        
        node = Node()
        node.decision_attribute = best_attribute
        node.name = attribute_metadata[best_attribute]['name']
        node.is_nominal = attribute_metadata[best_attribute]['is_nominal']
        node.value = attribute_modes_dict[best_attribute]
        updated_numerical_splits_count = copy.deepcopy(numerical_splits_count)
        updated_numerical_splits_count[best_attribute] -= 1

        if node.is_nominal:
            examples = split_on_nominal(data_set, best_attribute)
            for key, values in examples.items():
                node.children[key] = ID3_recursive(values, attribute_metadata, updated_numerical_splits_count, depth - 1, attribute_modes_dict)
        else:
            node.splitting_value = split_value
            (less, greater_or_equal) = split_on_numerical(data_set, best_attribute, split_value)
            node.children[0] = ID3_recursive(less, attribute_metadata, updated_numerical_splits_count, depth - 1, attribute_modes_dict)
            node.children[1] = ID3_recursive(greater_or_equal, attribute_metadata, updated_numerical_splits_count, depth - 1, attribute_modes_dict)
        
        return node
        
def default_node(data_set):
    node = Node()
    node.label = mode(data_set)
    return node

def attribute_modes(data_set, attribute_metadata):
    attr_dict = {}
    iterator = enumerate(attribute_metadata)
    next(iterator) # skip first
    for idx, attribute in iterator:
        attribute_data_set = []
        for example in data_set:
            if example[idx] is not None:
                attribute_data_set.append([example[idx]])
        if attribute['is_nominal']:        
            attr_dict[idx] = mode(attribute_data_set)
        else:
            attr_sum = sum(x[0] for x in attribute_data_set)
            attr_dict[idx] = attr_sum/float(len(attribute_data_set))
    return attr_dict      

def check_homogenous(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Checks if the output value (index 0) is the same for all examples in the the data_set, if so return that output value, otherwise return None.
    ========================================================================================================
    Output: Return either the homogenous attribute or None
    ========================================================================================================
     '''
    test_value = data_set[0][0]
    for example in data_set:
        if example[0] != test_value:
            return None
    return test_value 
# ======== Test Cases =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  None
# data_set = [[0],[1],[None],[0]]
# check_homogenous(data_set) ==  None
# data_set = [[1],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  1

def pick_best_attribute(data_set, attribute_metadata, numerical_splits_count):
    '''
    ========================================================================================================
    Input:  A data_set, attribute_metadata, splits counts for numeric
    ========================================================================================================
    Job:    Find the attribute that maximizes the gain ratio. If attribute is numeric return best split value.
            If nominal, then split value is False.
            If gain ratio of all the attributes is 0, then return False, False
            Only consider numeric splits for which numerical_splits_count is greater than zero
    ========================================================================================================
    Output: best attribute, split value if numeric
    ========================================================================================================
    '''
    best_attribute = {'index': None, 'gain_ratio': 0, 'split_value': None}
    iterator = enumerate(attribute_metadata)
    next(iterator) # skip first
    for idx, attribute in iterator:
        if attribute['is_nominal'] == True:
            gain_ratio = gain_ratio_nominal(data_set, idx)
            if gain_ratio > best_attribute['gain_ratio']:
                best_attribute['index'] = idx
                best_attribute['gain_ratio'] = gain_ratio
                best_attribute['split_value'] = False
        else:
            if numerical_splits_count[idx] > 0:
                gain_ratio, split_value = gain_ratio_numeric(data_set, idx, 1)
                if gain_ratio > best_attribute['gain_ratio']:
                    best_attribute['index'] = idx
                    best_attribute['gain_ratio'] = gain_ratio
                    best_attribute['split_value'] = split_value
    return (best_attribute['index'], best_attribute['split_value']) if best_attribute['gain_ratio'] != 0 else (False, False)                

# # ======== Test Cases =============================
# numerical_splits_count = [20,20]
# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "opprundifferential",'is_nominal': False}]
# data_set = [[1, 0.27], [0, 0.42], [0, 0.86], [0, 0.68], [0, 0.04], [1, 0.01], [1, 0.33], [1, 0.42], [0, 0.51], [1, 0.4]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, 0.51)
# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "weather",'is_nominal': True}]
# data_set = [[0, 0], [1, 0], [0, 2], [0, 2], [0, 3], [1, 1], [0, 4], [0, 2], [1, 2], [1, 5]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, False)

# Uses gain_ratio_nominal or gain_ratio_numeric to calculate gain ratio.

def mode(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Takes a data_set and finds mode of index 0.
    ========================================================================================================
    Output: mode of index 0.
    ========================================================================================================
    '''
    frequencies = {}
    for example in data_set:
        count = frequencies.get(example[0], 0)
        count += 1
        frequencies[example[0]] = count
    return max(frequencies.iterkeys(), key=(lambda k: frequencies[k]))
# ======== Test case =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# mode(data_set) == 1
# data_set = [[0],[1],[0],[0]]
# mode(data_set) == 0

def entropy(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Calculates the entropy of the attribute at the 0th index, the value we want to predict.
    ========================================================================================================
    Output: Returns entropy. See Textbook for formula
    ========================================================================================================
    '''
    total = 0
    n0 = 0
    n1 = 0
    for example in data_set:
        total += 1
        if example[0] == 0:
            n0 += 1
        elif example[0] == 1:
            n1 += 1

    if total == 0:
        return 0

    p0 = n0/float(total)
    p1 = n1/float(total)
    log0 = math.log(p0, 2) if p0 != 0.0 else 0.0
    log1 = math.log(p1, 2) if p1 != 0.0 else 0.0

    return -p0*log0 - p1*log1



# ======== Test case =============================
# data_set = [[0],[1],[1],[1],[0],[1],[1],[1]]
# entropy(data_set) == 0.811
# data_set = [[0],[0],[1],[1],[0],[1],[1],[0]]
# entropy(data_set) == 1.0
# data_set = [[0],[0],[0],[0],[0],[0],[0],[0]]
# entropy(data_set) == 0


def gain_ratio_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  Subset of data_set, index for a nominal attribute
    ========================================================================================================
    Job:    Finds the gain ratio of a nominal attribute in relation to the variable we are training on.
    ========================================================================================================
    Output: Returns gain_ratio. See https://en.wikipedia.org/wiki/Information_gain_ratio
    ========================================================================================================
    '''
    attr_values = split_on_nominal(data_set, attribute)
    entropy_sum = 0.0
    intrinsic_value = 0.0
    for val in attr_values.keys():
        p = len(attr_values[val])/float(len(data_set))
        entropy_sum += p*entropy(attr_values[val])
        intrinsic_value -= p*math.log(p, 2)
    information_gain = entropy(data_set) - entropy_sum
    return information_gain/intrinsic_value if intrinsic_value != 0.0 else 0

# ======== Test case =============================
# data_set, attr = [[1, 2], [1, 0], [1, 0], [0, 2], [0, 2], [0, 0], [1, 3], [0, 4], [0, 3], [1, 1]], 1
# gain_ratio_nominal(data_set,attr) == 0.11470666361703151
# data_set, attr = [[1, 2], [1, 2], [0, 4], [0, 0], [0, 1], [0, 3], [0, 0], [0, 0], [0, 4], [0, 2]], 1
# gain_ratio_nominal(data_set,attr) == 0.2056423328155741
# data_set, attr = [[0, 3], [0, 3], [0, 3], [0, 4], [0, 4], [0, 4], [0, 0], [0, 2], [1, 4], [0, 4]], 1
# gain_ratio_nominal(data_set,attr) == 0.06409559743967516

def gain_ratio_numeric(data_set, attribute, steps):
    '''
    ========================================================================================================
    Input:  Subset of data set, the index for a numeric attribute, and a step size for normalizing the data.
    ========================================================================================================
    Job:    Calculate the gain_ratio_numeric and find the best single threshold value
            The threshold will be used to split examples into two sets
                 those with attribute value GREATER THAN OR EQUAL TO threshold
                 those with attribute value LESS THAN threshold
            Use the equation here: https://en.wikipedia.org/wiki/Information_gain_ratio
            And restrict your search for possible thresholds to examples with array index mod(step) == 0
    ========================================================================================================
    Output: This function returns the gain ratio and threshold value
    ========================================================================================================
    '''
    threshold = {}
    for index in xrange(0, len(data_set), steps):
        value = data_set[index][attribute]
        threshold[value] = None

    for value in threshold.keys():
        less, greater_or_equal = split_on_numerical(data_set, attribute, value)
        if len(less) > 0 and len(greater_or_equal) > 0:
            entropy_sum = 0.0
            intrinsic_value = 0.0
            for value_list in [less, greater_or_equal]:
                p = len(value_list)/float(len(data_set))
                entropy_sum += p*entropy(value_list)
                intrinsic_value -= p*math.log(p, 2)
            information_gain = entropy(data_set) - entropy_sum
            threshold[value] = information_gain/intrinsic_value

    value = max(threshold.iterkeys(), key=(lambda k: threshold[k]))
    return (threshold[value], value)


# ======== Test case =============================
# data_set,attr,step = [[0,0.05], [1,0.17], [1,0.64], [0,0.38], [0,0.19], [1,0.68], [1,0.69], [1,0.17], [1,0.4], [0,0.53]], 1, 2
# gain_ratio_numeric(data_set,attr,step) == (0.31918053332474033, 0.64)
# data_set,attr,step = [[1, 0.35], [1, 0.24], [0, 0.67], [0, 0.36], [1, 0.94], [1, 0.4], [1, 0.15], [0, 0.1], [1, 0.61], [1, 0.17]], 1, 4
# gain_ratio_numeric(data_set,attr,step) == (0.11689800358692547, 0.94)
# data_set,attr,step = [[1, 0.1], [0, 0.29], [1, 0.03], [0, 0.47], [1, 0.25], [1, 0.12], [1, 0.67], [1, 0.73], [1, 0.85], [1, 0.25]], 1, 1
# gain_ratio_numeric(data_set,attr,step) == (0.23645279766002802, 0.29)

def split_on_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  subset of data set, the index for a nominal attribute.
    ========================================================================================================
    Job:    Creates a dictionary of all values of the attribute.
    ========================================================================================================
    Output: Dictionary of all values pointing to a list of all the data with that attribute
    ========================================================================================================
    '''
    attr_dict = {}
    for example in data_set:
        key = example[attribute]
        if attr_dict.has_key(key):
            attr_dict[key].append(example)
        else:
            attr_dict[key] = [example]
    return attr_dict

# ======== Test case =============================
# data_set, attr = [[0, 4], [1, 3], [1, 2], [0, 0], [0, 0], [0, 4], [1, 4], [0, 2], [1, 2], [0, 1]], 1
# split_on_nominal(data_set, attr) == {0: [[0, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3]], 4: [[0, 4], [0, 4], [1, 4]]}
# data_set, attr = [[1, 2], [1, 0], [0, 0], [1, 3], [0, 2], [0, 3], [0, 4], [0, 4], [1, 2], [0, 1]], 1
# split on_nominal(data_set, attr) == {0: [[1, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3], [0, 3]], 4: [[0, 4], [0, 4]]}

def split_on_numerical(data_set, attribute, splitting_value):
    '''
    ========================================================================================================
    Input:  Subset of data set, the index for a numeric attribute, threshold (splitting) value
    ========================================================================================================
    Job:    Splits data_set into a tuple of two lists, the first list contains the examples where the given
	attribute has value less than the splitting value, the second list contains the other examples
    ========================================================================================================
    Output: Tuple of two lists as described above
    ========================================================================================================
    '''
    less = []
    greater_or_equal = []
    for example in data_set:
        if example[attribute] < splitting_value:
            less.append(example)
        else:
            greater_or_equal.append(example)
    return (less, greater_or_equal)        

# ======== Test case =============================
# d_set,a,sval = [[1, 0.25], [1, 0.89], [0, 0.93], [0, 0.48], [1, 0.19], [1, 0.49], [0, 0.6], [0, 0.6], [1, 0.34], [1, 0.19]],1,0.48
# split_on_numerical(d_set,a,sval) == ([[1, 0.25], [1, 0.19], [1, 0.34], [1, 0.19]],[[1, 0.89], [0, 0.93], [0, 0.48], [1, 0.49], [0, 0.6], [0, 0.6]])
# d_set,a,sval = [[0, 0.91], [0, 0.84], [1, 0.82], [1, 0.07], [0, 0.82],[0, 0.59], [0, 0.87], [0, 0.17], [1, 0.05], [1, 0.76]],1,0.17
# split_on_numerical(d_set,a,sval) == ([[1, 0.07], [1, 0.05]],[[0, 0.91],[0, 0.84], [1, 0.82], [0, 0.82], [0, 0.59], [0, 0.87], [0, 0.17], [1, 0.76]])