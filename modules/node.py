# DOCUMENTATION
# =====================================
# Class node attributes:
# ----------------------------
# children - a list of 2 nodes if numeric, and a dictionary (key=attribute value, value=node) if nominal.  
#            For numeric, the 0 index holds examples < the splitting_value, the 
#            index holds examples >= the splitting value
#
# label - is None if there is a decision attribute, and is the output label (0 or 1 for
#	the homework data set) if there are no other attributes
#       to split on or the data is homogenous
#
# decision_attribute - the index of the decision attribute being split on
#
# is_nominal - is the decision attribute nominal
#
# value - Ignore (not used, output class if any goes in label)
#
# splitting_value - if numeric, where to split
#
# name - name of the attribute being split on
import copy

class Node:
    def __init__(self):
        # initialize all attributes
        self.label = None
        self.decision_attribute = None
        self.is_nominal = None
        self.value = None
        self.splitting_value = None
        self.children = {}
        self.name = None

    def classify(self, instance):
        '''
        given a single observation, will return the output of the tree
        '''
        if self.label == None:
            key = instance[self.decision_attribute]
            if key == None:
                # mode  is stored in value
                key = self.value
            if self.is_nominal == True:
                child = self.children.get(key, self.children.get(self.value, None))
                if child == None:
                    child = self.children.values()[0]
                return child.classify(instance)
            else:
                if key < self.splitting_value:
                    return self.children[0].classify(instance)
                else:
                    return self.children[1].classify(instance)
        return self.label 

    def print_tree(self, indent = 0):
        '''
        returns a string of the entire tree in human readable form
        IMPLEMENTING THIS FUNCTION IS OPTIONAL
        '''
        # Your code here
        pass

    def print_dnf_tree(self):
        def dnf_tree_path(node, current_path, paths):
            if node.label is not None:
                if node.label == 1:
                    paths.append(current_path)
                    return copy.deepcopy(paths)
                else:
                    return []
            else:
                current_path_and = current_path
                if current_path != '':
                    current_path_and += ' ^ '
                if node.is_nominal:
                    nominal_paths = []
                    for key in node.children.keys():
                        nominal_path = current_path_and + node.name + '=' + str(key)
                        nominal_dnf = dnf_tree_path(node.children[key], nominal_path, copy.deepcopy(paths))
                        if len(nominal_dnf) > 0:
                            nominal_paths += nominal_dnf
                    return nominal_paths        
                else:
                    less_path = current_path_and + node.name + '<' + str(node.splitting_value)
                    greater_or_equal_path = current_path_and + node.name + '>=' + str(node.splitting_value)
                    return dnf_tree_path(node.children[0], less_path, copy.deepcopy(paths)) + dnf_tree_path(node.children[1], greater_or_equal_path, copy.deepcopy(paths))
        
        paths = dnf_tree_path(self, '', [])
        if len(paths) == 0:
            print 'No DNF'
        elif len(paths) == 1:
            print paths[0]
        elif len(paths) > 1:
            print '(' + ') + ('.join(paths) + ')'        
