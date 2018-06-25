from CONFIG import *

class Node(object):
    """
    Class Node
    """
    def __init__(self, item_type):
        self.left = None
        self.middle = None
        self.right = None
        self.item_type = item_type # the value of the current item type.

    def get_node_item_type(self):
        return self.item_type

    def get_node_left(self):
        return self.left

    def get_node_right(self):
        return self.right

    def get_node_mid(self):
        return self.middle


class Tree(object):
    """
    Class tree will provide a tree as well as utility functions.
    """

    def create_node(self, item_type):
        """
        Utility function to create a node.
        """
        return Node(item_type)

    def insert_state(self, node, item_type):
        """
        Insert function will insert a node into tree.
        Duplicate keys are not allowed.
        """
        #if tree is empty , return a root node
        if node is None:
            return Node(item_type)
        # if data is smaller than parent , insert it into left side
        if item_type == 1:
            node.left = self.insert(node.left, item_type)
        elif item_type == 3:
            node.left = self.insert(node.right, item_type)
        else:
            node.middle = self.insert(node.middle, item_type)
        return node


    def search(self, node, data):
        """
        Search function will search a node into tree.
        """
        # if root is None or root is the search data.
        if node is None or node.data == data:
            return node

        if node.data < data:
            return self.search(node.right, data)
        else:
            return self.search(node.left, data)



    def deleteNode(self,node,data):
        """
        Delete function will delete a node into tree.
        Not complete , may need some more scenarion that we can handle
        Now it is handling only leaf.
        """

        # Check if tree is empty.
        if node is None:
            return None

        # searching key into BST.
        if data < node.data:
            node.left = self.deleteNode(node.left, data)
        elif data > node.data:
            node.right = self.deleteNode(node.right, data)
        else: # reach to the node that need to delete from BST.
            if node.left is None and node.right is None:
                del node
            if node.left == None:
                temp = node.right
                del node
                return  temp
            elif node.right == None:
                temp = node.left
                del node
                return temp

        return node






    def traverseInorder(self, root):
        """
        traverse function will print all the node in the tree.
        """
        if root is not None:
            self.traverseInorder(root.left)
            print root.data
            self.traverseInorder(root.right)

    def traversePreorder(self, root):
        """
        traverse function will print all the node in the tree.
        """
        if root is not None:
            print root.data
            self.traversePreorder(root.left)
            self.traversePreorder(root.right)

    def traversePostorder(self, root):
        """
        traverse function will print all the node in the tree.
        """
        if root is not None:
            self.traversePreorder(root.left)
            self.traversePreorder(root.right)
            print root.data


def relax_queue(queue_items):
    queue_dict = dict(queue_items)
    for k in ITEMS_NAMES:
        if queue_dict[k] == 0:
            pass
        elif queue_dict[k] <= 3:
            queue_dict[k] = 3
        elif queue_dict[k] <= 10:
            queue_dict[k] = 10
        else:
            queue_dict[k] = 20
    return queue_dict


def compare_two_states(s1, s2):
    simlar_states = False
    # check if items in the production line are in the same order:
    if s1[0][0] == s2[0][0]:
        # check if the locations of the items in the production line are close:
        if bin_loc(s1[0][1]) == bin_loc(s2[0][1]):
            if relax_queue(s1[1]) == relax_queue(s2[1]):
                simlar_states = True
    return simlar_states


def bin_loc(locs, d=5):
    relax_locs = []
    for l in locs:
        for j in np.arange(0, 40 + d, d):
            if l <= j:
                relax_locs.append(j)
                break
    return relax_locs


def get_similar_states_idx(visited_states, some_state):
    similar_states = []
    for i in range(len(visited_states)):
        if compare_two_states(visited_states[i], some_state):
            similar_states.append(i)
    return similar_states


#
# def divide_queues_types(visited_states, n=2):
#     """
#     visited_states - list - describe state:
#      - items in system, with locations.
#      - items in queue
#      - immidiate reward
#     n - number of minimum items per type
#     """
#     type1_states = []
#     type2_states = []
#     for s in visited_states:
#         if len([i for i in s[1] if i[1] > n]) == 3:
#             type1_states.append(s)
#         else:
#             type2_states.append(s)
#     print len(type1_states), len(type2_states)
#     return type1_states, type2_states