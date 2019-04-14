from util import entropy, information_gain, partition_classes
import numpy as np 
import ast

class DecisionTree(object):
    def __init__(self):
        # Initializing the tree as an empty dictionary or list, as preferred
        #self.tree = []
        self.tree = {}
        # pass
        return

    def optimizeCurrentAttributeGain(self, X, y, current_attr):
        max_gain = 0
        max_split_point = 0
        values, _ = np.unique(X, return_counts=True)
        
        for split_point in values:
            _, _, y_left, y_right, _ = partition_classes(X,y,current_attr,split_point)
            gain = information_gain(y,[y_left, y_right])

            if gain > max_gain: 
                max_gain = gain
                max_split_point = split_point

        return max_split_point

    def learn(self, X, y, visited=[]):
        # TODO: Train the decision tree (self.tree) using the the sample X and labels y
        # You will have to make use of the functions in utils.py to train the tree
        
        # One possible way of implementing the tree:
        #    Each node in self.tree could be in the form of a dictionary:
        #       https://docs.python.org/2/library/stdtypes.html#mapping-types-dict
        #    For example, a non-leaf node with two children can have a 'left' key and  a 
        #    'right' key. You can add more keys which might help in classification
        #    (eg. split attribute and split value)
        
        # Handle case when all conditions have been tested
        if len(y) == 0:
            self.tree["label"] = "failure"
            return

        # Handle case when the tree reaches the leaf node
        values, counts = np.unique(y,return_counts=True)
        ind = np.argmax(counts)
        if len(visited) == len(X[0]) or len(counts) == 1:
            self.tree["label"] = "leaf"
            self.tree["value"] = values[ind]
            return

        # Find node with max gain
        max_gain = 0
        max_index = 0
        max_index_type = ""
        X_left = []
        X_right = []
        y_left = []
        y_right = []

        for curr_attr in range(len(X[0])):

            split_point = self.optimizeCurrentAttributeGain(X,y,curr_attr)
            X_l, X_r, y_l, y_r, attr_type = partition_classes(X,y,curr_attr,split_point)
            gain = information_gain(y,[y_l, y_r])

            if gain > max_gain:
                max_gain = gain
                max_index = curr_attr
                X_left = X_l
                X_right = X_r
                y_left = y_l
                y_right = y_r
                max_index_type = attr_type
        
        subtreeLeft = DecisionTree()
        subtreeRight = DecisionTree()
        subtreeLeft.learn(X_left, y_left, visited)
        subtreeRight.learn(X_right, y_right, visited)
        self.tree["label"] = "node"
        self.tree["attr"] = max_index
        self.tree["attr_type"] = max_index_type
        self.tree["split"] = self.optimizeCurrentAttributeGain(X,y,max_index)
        self.tree["left_child"] = subtreeLeft
        self.tree["right_child"] = subtreeRight  
        return


    def classify(self, record):
        # TODO: classify the record using self.tree and return the predicted label
        if self.tree["label"] == "failure":
            return 0
        elif self.tree["label"] == "leaf":
            return self.tree["value"]
        elif self.tree["label"] == "node":
            if self.tree["attr_type"] == "continuous":
                if record[self.tree["attr"]] <= self.tree["split"]:
                    return self.tree["left_child"].classify(record)
                else:
                    return self.tree["right_child"].classify(record)
            else: # self.tree["attr_type"] == "categorical"
                if record[self.tree["attr"]] == self.tree["split"]:
                    return self.tree["left_child"].classify(record)
                else:
                    return self.tree["right_child"].classify(record)

