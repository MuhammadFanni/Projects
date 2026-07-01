"""A class represnting a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type key: int or None
    @param key: key of your node
    @type value: any
    @param value: data of your node
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        if key is None:
            self.left = None
            self.right = None
            self.parent = None
            self.height = -1
            self.size = 0
        else:
            self.left = AVLNode(None, None)
            self.right = AVLNode(None, None)
            self.left.parent = self
            self.right.parent = self
            self.parent = None
            self.update_height()
            self.update_size()


    """sets key

    @type key: int or None
    @param key: key
    """

    def set_key(self, key):
        self.key = key

    """sets value

    @type value: any
    @param value: data
    """

    def set_value(self, value):
        self.value = value

    """sets left child

    @type node: AVLNode
    @param node: a node
    """

    def set_left(self, node):
        if self.is_real_node() is False:
            return None

        if node is None:
            self.set_left(AVLNode(None, None))

        # self.left.set_parent(None)
        self.left = node
        self.left.set_parent(self)
        self.update_fields()

        return None

    """sets right child

    @type node: AVLNode
    @param node: a node
    """

    def set_right(self, node):
        if self.is_real_node() is False:
            return None

        if node is None:
            self.set_right(AVLNode(None, None))

        # self.right.set_parent(None)
        self.right = node
        self.right.set_parent(self)
        self.update_fields()

        return None

    """sets parent

    @type node: AVLNode
    @param node: a node
    """

    def set_parent(self, node):
        if self:
            self.parent = node

    """sets the height of the node

    @type h: int
    @param h: the height
    """

    def set_height(self, h):
        self.height = h
        return None

    """updates the height of the node"""
    def update_height(self):
        if self.is_real_node is False:
            self.set_height(-1)
            return None
        self.set_height(max(self.right.height, self.left.height) + 1)

        return None

    """sets the size of node

    @type s: int
    @param s: the size
    """

    def set_size(self, s):
        self.size = s
        return None

    """updates the size of the node"""
    def update_size(self):
        if self.is_real_node is False:
            self.set_size(0)
            return None
        self.set_size(self.right.size + self.left.size + 1)

        return None

    """updates the fields of the node"""
    def update_fields(self):
        self.update_size()
        self.update_height()

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def is_real_node(self):
        if not self:
            return False
        if self.key is not None:
            return True
        return False

    """returns the BF of the node 

        @rtype: int
        @returns: number representation of balance factor of the node.
        """
    def get_BF(self):
        if self.is_real_node():
            return self.left.height - self.right.height

    """returns if the node is a right child 

           @rtype: bool
           @returns: True if the node is a right child, False otherwise.
           """
    def is_right_child(self, node):
        return self.right is node

    """returns if the node has a left child 

               @rtype: bool
               @returns: True if the node has a left child, False otherwise.
               """
    def has_left_child(self):
        return self.left.is_real_node()

    """returns if the node has a right child 

                   @rtype: bool
                   @returns: True if the node has a right child, False otherwise.
                   """
    def has_right_child(self):
        return self.right.is_real_node()

    """returns if the node is a leaf (has children)
    
                       @rtype: bool
                       @returns: True if the node is a leaf, False otherwise.
                       """
    def is_leaf(self):
        return (not self.right.is_real_node()) and (not self.left.is_real_node())


"""
A class implementing an AVL tree.
"""


class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.
    min is the smallest element in the tree.
    root is the root of the tree.
    """

    def __init__(self):
        self.root = None
        self.min = AVLNode(9223372036854775807, None)

    """searches for a node in the dictionary corresponding to the key
    
    @type key: int
    @param key: a key to be searched
    @rtype: AVLNode
    @returns: node corresponding to key
    """

    def search(self, key):
        curr = self.root
        if curr is None:
            return None
        while curr.is_real_node():
            curr_key = curr.key
            if curr_key == key:
                return curr
            if curr_key > key:
                curr = curr.left
            else:
                curr = curr.right

        return None

    """inserts a new node into the dictionary with corresponding key and value

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def insert(self, key, val):
        if self:
            node = AVLNode(key, val)
            return self.insert_node(node)

    """inserts given node into the dictionary 

        @type Node: AVLNode
        @rtype: int
        @returns: the number of rebalancing operation due to AVL rebalancing
        """

    def insert_node(self, node):
        if self.min.key > node.key:
            self.min = node

        old_height = self.insert_bts(node)

        curr = node.parent
        cnt = 0 #counter for rebalancing operation due to AVL rebalancing
        while curr is not None:
            if curr is not node.parent:
                old_height = curr.height
            curr.update_fields()
            curr_BF = curr.get_BF()

            if abs(curr_BF) < 2 and old_height == curr.height:
                curr = curr.parent
                continue
            if abs(curr_BF) < 2 and old_height != curr.height:
                cnt += 1
                curr = curr.parent
                continue
            if abs(curr_BF) == 2:
                root = curr
                curr = root.parent
                cnt += self.rotate(root, curr_BF)
                continue
        return cnt

    """rotates the tree if needed, to keep it an AVLTree

           @type Node: AVLNode
           @type node_BF: int
           @rtype: int
           @returns: the number of rotations
        """
    def rotate(self, node, node_BF):
        left_BF = node.left.get_BF()
        right_BF = node.right.get_BF()
        if node_BF == 2:
            if left_BF == 1 or left_BF == 0:
                self.right_rotation(node)
                return 1
            if left_BF == -1:
                self.left_rotation(node.left)
                self.right_rotation(node)
                return 2
        elif node_BF == -2:
            if right_BF == 1:
                self.right_rotation(node.right)
                self.left_rotation(node)
                return 2
            if right_BF == -1 or right_BF == 0:
                self.left_rotation(node)
                return 1
        return 0

    """rotates the tree to the right, to keep it an AVLTree

               @type Node: AVLNode
        """
    def right_rotation(self, node):

        node_left = node.left
        node_parent = node.parent

        node.set_left(node_left.right)
        node.update_fields()
        node_left.set_right(node)
        node_left.update_fields()

        if node_parent is None:
            node_left.set_parent(None)
            self.root = node_left
        else:
            node_is_right_child = node_parent.is_right_child(node)
            if node_is_right_child:
                node_parent.set_right(node_left)
            else:
                node_parent.set_left(node_left)
            return None
        """rotates the tree to the left, to keep it an AVLTree

                @type Node: AVLNode
        """
    def left_rotation(self, node):

        node_right = node.right
        node_parent = node.parent

        node.set_right(node_right.left)
        node.update_fields()
        node_right.set_left(node)
        node_right.update_fields()

        if node_parent is None:
            node_right.set_parent(None)
            self.root = node_right
        else:
            node_is_right_child = node_parent.is_right_child(node)
            if node_is_right_child:
                node_parent.set_right(node_right)
            else:
                node_parent.set_left(node_right)
            return None

    """inserts node is we would in normal BTS, returns node parent old height
            @type Node: AVLNode
            @rtype: int
    """
    def insert_bts(self, node):
        if not AVLNode.is_real_node(self.get_root()):
            self.root = node
            return -2
        curr = self.get_root()
        my_side = None  # False -> im left child,else im right child
        temp = curr
        while curr.is_real_node():
            temp = curr.parent

            if node.key < curr.key:
                temp = curr
                curr = curr.left
                my_side = False
            else:
                temp = curr
                curr = curr.right
                my_side = True
        curr = temp
        parent_old_height = curr.height
        if my_side is True:
            curr.set_right(node)
        else:
            curr.set_left(node)
        return parent_old_height

    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def delete(self, node):
        # update min
        if node is self.min:
            new_min = self.successor(node)
            if new_min is None: new_min = AVLNode(9223372036854775807, None)
            self.min = new_min

        y, old_height = self.delete_bts(node)
        # here y is the parent of the physically deleted node, or the parent of the parent of the physically deleted node
        cnt = 0  # rebalancing operations counter
        while y is not None:
            y.update_fields()
            y_BF = y.get_BF()
            if abs(y_BF) < 2 and (y.height == old_height):
                y = y.parent
                continue
            elif abs(y_BF) < 2 and (y.height != old_height):
                y = y.parent
                old_height = y.height if y is not None else -2
                cnt += 1
                continue
            elif abs(y_BF) == 2:
                temp = y
                y = y.parent
                old_height = y.height if y is not None else -2
                cnt += self.rotate(temp, y_BF)
                continue

        return cnt

    """ deletes node from BST(without balancing), 
        returns the physically deleted node's parent and it's old_height
            @type node: AVLNode
            @rtype: tuple
    """

    def delete_bts(self, node):

        if node is None: return (None, -2)
        if not node.is_real_node(): return (None, -2)
        if node.is_leaf():
            return self.delete_case_1(node)

        elif not node.left.is_real_node():
            return self.delete_case_2(node)

        elif not node.right.is_real_node():
            return self.delete_case_2(node)

        else:  # has right and hase left
            return self.delete_case_3(node)

    """returns deleted node and it's parent_old_height
        @pre: node is real leaf node
    """
    def delete_case_1(self, node):
        if self.get_root() is node:
            self.root = None
            AVLNode(9223372036854775807, None)
            return (None, -2)

        parent_old_height = node.parent.height
        parent = node.parent
        if parent.key < node.key:
            parent.set_right(AVLNode(None, None))
        elif parent.key > node.key:
            parent.set_left(AVLNode(None, None))

        node.set_parent(None)
        node.update_fields()
        parent.update_fields()
        return (parent, parent_old_height)

    """returns deleted node and it's parent_old_height
           @pre: node is real leaf node
       """
    def delete_case_2(self, node):
        if self.get_root() is node:
            if node.right.is_real_node():
                self.root = node.right
            else:  # node.left.is_real_node()
                self.root = node.left

        # update pointers
        parent = node.parent
        if parent is None:
            # node is the root of self
            self.root.parent = None
            parent_old_height = -2
        else:
            parent_old_height = node.parent.height
            if parent.right is node:  # node is a right child (case2_Right)
                if node.right.is_real_node():
                    parent.set_right(node.right)
                    node.set_right(AVLNode(None, None))
                else:  # node.left.is_real_node()
                    parent.set_right(node.left)
                    node.set_left(AVLNode(None, None))

            else:  # node is a left child (case2_Left)
                if node.right.is_real_node():
                    parent.set_left(node.right)
                    node.set_right(AVLNode(None, None))
                else:  # node.left.is_real_node()
                    parent.set_left(node.left)
                    node.set_left(AVLNode(None, None))

        node.set_parent(None)
        return (parent, parent_old_height)

    """returns deleted successor and it's parent_old_height
           @pre: node hase 2 childs and not the root
       """
    def delete_case_3(self, node):
        succ = self.successor(node)
        # observation: succ hase no left child
        # observation: succ have parent (he is not the root)
        # observation: succ exists (real node)

        # succ parent and height
        succ_old_height = succ.height
        succ_parent_old_height = succ.parent.height
        succ_parent = succ.parent
        check_succ = False
        if succ_parent is node:
            check_succ = True
            succ_parent = node.parent
        if succ.is_leaf():
            self.delete_case_1(succ)
        else:
            self.delete_case_2(succ)

        # replace node and succ
        if node.parent is None:
            succ.set_parent(None)
            succ_parent_old_height = -2
        elif node.parent.key < succ.key:
            node.parent.set_right(succ)
        else:
            node.parent.set_left(succ)
        succ.set_left(node.left)
        succ.set_right(node.right)
        if self.get_root() is node:
            self.root = succ
        node.set_parent(None)
        node.set_right(AVLNode(None, None))
        node.set_left(AVLNode(None, None))

        if check_succ:
            return (succ, succ_old_height)
        else:
            return (succ_parent, succ_parent_old_height)

    """returns the successor of the given node
        @pre: node is a real node
        @rtype: AVLNode
        @returns: the next successor of the given node
        """
    def successor(self, node):
        if node.has_right_child():
            curr = node.right
            while curr.left.is_real_node():
                curr = curr.left
            return curr
        else:
            curr = node
            while (curr.parent is not None) and (curr.parent.is_right_child(curr)):
                curr = curr.parent
        return curr.parent

    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of touples (key, value) representing the data structure
    """

    # takes an AVLTree tree and returns the minimum node in the tree
    def min_in_tree(self):
        curr = self.root
        if curr is None:
            return AVLNode(9223372036854775807, None)
        while curr.left.is_real_node():
            curr = curr.left
        return curr

    def avl_to_array(self):
        if self.root is None:
            return []
        length = self.size()
        array = [None] * length
        curr = self.min_in_tree()
        for i in range(length):
            array[i] = (curr.key, curr.value)
            curr = self.successor(curr)
        return array

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """

    def size(self):
        if self.get_root() is None:
            return 0
        return self.get_root().size

    """compute the rank of node in the dictionary

    	@type node: AVLNode
    	@pre: node is in self
    	@param node: a node in the dictionary to compute the rank for
    	@rtype: int
    	@returns: the rank of node in self
    """

    def rank(self, node):
        rank_node = node.left.size + 1
        curr = self.get_root()

        while curr is not node:

            if curr.key < node.key:
                rank_node += curr.left.size + 1
                curr = curr.right
                continue
            curr = curr.left

        return rank_node

    """finds the i'th smallest item (according to keys) in self

    @type i: int
    @pre: 1 <= i <= self.size()
    @param i: the rank to be selected in self
    @rtype: int
    @returns: the item of rank i in self
    """

    def select(self, i):
        if self.root is None:
            return None
        curr = self.get_root()
        while curr.is_real_node():
            cnt = curr.left.size + 1  # num of nodes =< curr
            if cnt == i:
                return curr
            elif cnt < i:
                curr = curr.right
                i = i - cnt
            elif cnt > i:
                curr = curr.left

    """finds the node with the largest value in a specified range of keys

    	@type a: int
    	@param a: the lower end of the range
    	@type b: int
    	@param b: the upper end of the range
    	@pre: a<b
    	@rtype: AVLNode
    	@returns: the node with maximal (lexicographically) value having a<=key<=b, or None if no such keys exist
    """

    def max_range(self, a, b):
        max_node = self.rec_max_range(self.root, a, b, None)
        return max_node.value if max_node else None

    def rec_max_range(self, node, a, b, max_node):
        if not node or not node.is_real_node:
            return max_node

        if a < node.key:
            max_node = self.rec_max_range(node.left, a, b, max_node)
        if a <= node.key <= b:
            if not max_node or node.value > max_node.value:
                max_node = node
        if b > node.key:
            max_node = self.rec_max_range(node.right, a, b, max_node)

        return max_node




    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """

    def get_root(self):
        return self.root
