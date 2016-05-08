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
            if self.is_nominal == True:
                return self.children[key].classify(instance)
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
        '''
        returns the disjunct normalized form of the tree.
        '''
        def dnf_helper(node, string):
            if node.label != None:
                if node.label != 0:
                    return string
                else:
                    return None
            else:
                strings = []
                if node.is_nominal:
                    for key in node.children.keys():
                        passdown = string + ' ^ ' + node.name + '=' + key + ' ^ '
                        passup = dnf_helper(node.children[key], passdown)
                        if passup != None:
                            strings.append(passup)
                    for s in strings:
                        string += ' v ' + s
                    return string
                else:
                    for x in range(0, 2):
                        passdown = string + ' ^ ' + node.name + '=' + x + ' ^ '
                        passup = dnf_helper(node.children[x], passdown)
                        if passup != None:
                            strings.append(passup)
                    for s in strings:
                        string += ' v ' + s
                    return string

        return dnf_helper(self, "")