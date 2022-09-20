import numpy as np


def entropy(y):
    # get unique labels
    labels = np.unique(y[:])

    # sum over entropy given proportion of label to data
    ent = 0
    for l in labels:
        plabel = len(y[y == l]) / len(y)
        ent += -plabel * np.log2(plabel)
    return ent

def majority(y):
    # labels
    labels = np.unique(y)


def split_data(x, col_number):
    splits = {}
    vals = np.unique(x[:, col_number])
    for val in vals:
        subset = np.array([row for row in x if row[col_number] == val])
        # dont track empty subsets
        if len(subset) > 0:
            splits[val] = subset
    return splits


class Node:
    def __init__(self, data=None, split_idx=0, children=None, info_gain=-1, is_leaf=False):
        self.data = data
        self.split_idx = split_idx
        self.children = children
        self.info_gain = info_gain
        self.is_leaf = is_leaf

    def get_value(self):
        return

    ## could put most helper methods, especially purity measures, in node class


class DecisionTree:
    def __init__(self, data, mode="entropy", min_samples=2, max_depth=10):
        self.min_samples = min_samples
        self.max_depth = max_depth
        self.mode = mode

        self.root = self.build_tree(data)

    def build_tree(self, data, depth=0):
        # check the shape of the data to get the size of data
        num_samples = np.shape(data)[0]

        if depth <= self.max_depth and num_samples > self.min_samples:
            # set split_node to node of best split
            split_node = self.find_best_split(data)

            # node has no children or node is sorted
            if len(split_node.children) == 0 or split_node.info_gain == 0:
                split_node.is_leaf = True
                return split_node
            # node has children
            for key in split_node.children.keys():
                # replace the child data set with child tree
                split_node.children[key] = self.build_tree(split_node.children[key], depth+1)
            return split_node

        # if stopping conditions met, continues here
        return Node(data=data, is_leaf=True)

    def find_best_split(self, data):
        """Initializes node from data set. Sets node properties according to those that best split the node."""
        node = Node(data=data)
        max_gain = float('-inf')

        # split the data for each attribute and determine optimal split
        num_attr = data.shape[1] - 1
        for attr_idx in range(num_attr):
            # split data and compute info gain
            split = split_data(data, attr_idx)
            info_gain = self.info_gain(data, split.values())

            if info_gain > max_gain:
                # reset marker and initialize node properties
                max_gain = info_gain

                node.info_gain = info_gain
                node.split_idx = attr_idx
                node.children = split
        # returns node of best split
        return node

    def info_gain(self, pre_split, splits, mode="entropy"):
        """Calculates information gain from og data set to splits. pre_split should be ndarray with no column
        information, splits should be list of subsets of pre_split """
        # labels of data and splits
        Y = pre_split[:, -1]
        y = []

        # splits are subsets of pre_split based on value of single attribute
        # weight needed for each split
        num_splits = len(splits)
        weights = []
        for s in splits:
            s_lab = s[:, -1]
            y.append(s_lab)
            weights.append(len(s_lab) / len(Y))

        if self.mode == 'entropy':
            # entropy pre-split
            h_s = entropy(Y)

            # entropy after split
            h_split = 0
            for i in range(num_splits):
                h_split += weights[i] * entropy(y[i])

            return h_s - h_split

    def traverse_tree(self, node):
        curr_node = node
        if curr_node.is_leaf:
            return
        for key in curr_node.children.keys():
            self.traverse_tree(curr_node.children[key])