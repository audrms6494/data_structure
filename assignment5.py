


################################# Problem 1.1 #################################
class BinHeap:
    def __init__(self):
        self.heap_list = [0]
        self.current_size = 0
    
    ### CODE HERE ###
    def perc_up(self, i):  # Percolating up
        while i // 2 > 0:  # While parent exists
            change = False
            if self.heap_list[i] > self.heap_list[i//2]:  # if child is bigger than parent swap their value
                self.heap_list[i], self.heap_list[i//2] = self.heap_list[i//2], self.heap_list[i]
                change = True
            if not change:
                break
            i = i // 2  # Moving upwards
    
    def insert(self, k):
        self.heap_list.append(k)
        self.current_size = self.current_size + 1  # size up
        self.perc_up(self.current_size)  # Percolate up
    
    def perc_down(self, i):  # Percolating down
        while (i * 2) <= self.current_size:  # While child exists
            mc = self.max_child(i)
            change = False
            if self.heap_list[i] < self.heap_list[mc]:  # if one of child is bigger than parent swap their value
                self.heap_list[i], self.heap_list[mc] = self.heap_list[mc], self.heap_list[i]
                change = True
            if not change:
                break
            i = mc  # Moving downwards
    
    def max_child(self, i):  # used in perc_down
        if i * 2 + 1 > self.current_size:  # if there is only left child
            return i * 2
        else:
            if self.heap_list[i*2] > self.heap_list[i*2 + 1]:  # if left child is bigger
                return i * 2
            else:
                return i * 2 + 1
    
    def del_max(self):
        max_val = self.heap_list[1]
        self.heap_list[1] = self.heap_list[self.current_size]  # insert last component to root
        self.current_size -= 1  # size down
        self.heap_list.pop()  # delete the last value
        self.perc_down(1)  # percolate to find its position
        return max_val  # return deleted value

    def build_heap(self, a_list):  # used to build a heap from the list
        i = len(a_list) // 2  # percolate which has at least one child
        self.current_size = len(a_list)
        self.heap_list = [0] + a_list  # [0] : wasted element
        while i > 0:
            self.perc_down(i)
            i -= 1
    #################


################################################################################





################################# Problem 1.2 #################################

def find_median(lst):
    """ 
    This function finds and "prints" the medians of the all sublist, lst[0:i] using BinHeap.
    
    Args:
        lst (list) : The list of random integers.
    
    Returns:
        None
        
    """
    ### CODE HERE ###
    bh = BinHeap()  # Max heap => root = max value of small set
    temp = BinHeap()  # Min heap => root = min value of big set
    i = 1  # number of total components
    bh.insert(lst[0])  # insert first value
    print(lst[0])  # print that value
    for num in lst[1:]:
        i += 1
        if i%2 == 0:  # if number of components are even we insert in temp(Min heap)
            temp.insert(-num)  # make negative to make root minimum value
        else: # if it is odd we insert in bh (num of bh = num of temp + 1)
            bh.insert(num)
        if bh.heap_list[1] > -temp.heap_list[1]:  # if min value of big set is smaller than max value of small set
            temp.insert(-bh.del_max())  # delete and insert each other
            bh.insert(-temp.del_max())
        print(bh.heap_list[1])  # print median value which is max value of small set
    #################

################################################################################





################################## Problem 2 ###################################

# Do not touch anything in the Node class.
class Node:
    def __init__(self, key, left_child=None, right_child=None, parent=None):
        self.key = key
        self.left_child = left_child
        self.right_child = right_child
        self.parent = parent
        
    def has_left_child(self): 
        return self.left_child
    
    def has_right_child(self): 
        return self.right_child
    
    def is_left_child(self):
        return self.parent and self.parent.left_child == self
    
    def is_right_child(self):
        return self.parent and self.parent.right_child == self
    
    def is_root(self):
        return not self.parent
    
    def is_leaf(self):
        return not (self.right_child or self.left_child)
    
    def has_any_children(self):
        return self.right_child or self.left_child
    
    def has_both_children(self):
        return self.right_child and self.left_child


class SplayTree:
    def __init__(self):
        self.root = None
    
    def rotate(self, node): # used in splay method
        if node.is_left_child(): # if X is left child
            if node.has_right_child(): # if X has right child
                node.right_child.parent = node.parent # X's right child's parent : X => P
            node.parent.left_child = node.right_child # P's left child : X => B
            if node.parent.is_left_child(): # if P is left child
                node.parent = node.parent.parent # X's parent : P => G
                node.right_child = node.parent.left_child # X's right child : B => P  
                node.parent.left_child = node # G's left child is X
                node.right_child.parent = node # P's parent : G => X
            elif node.parent.is_right_child(): # if P is right child
                node.parent = node.parent.parent # X's parent : P => G
                node.right_child = node.parent.right_child # X's right child : B => P  
                node.parent.right_child = node # G's right child is X
                node.right_child.parent = node # P's parent : G => X
            else: # if P is root node
                node.right_child = node.parent
                node.right_child.parent = node
                node.parent = None
        elif node.is_right_child(): # if X is right child
            if node.has_left_child(): # if X has left child
                node.left_child.parent = node.parent # X's left child's parent : X => P
            node.parent.right_child = node.left_child # P's right child : X => B
            if node.parent.is_left_child(): # if P is left child
                node.parent = node.parent.parent # X's parent : P => G
                node.left_child = node.parent.left_child # X's right child : B => P  
                node.parent.left_child = node # G's left child is X
                node.left_child.parent = node # P's parent : G => X
            elif node.parent.is_right_child(): # if P is right child
                node.parent = node.parent.parent # X's parent : P => G
                node.left_child = node.parent.right_child # X's right child : B => P  
                node.parent.right_child = node # G's right child is X
                node.left_child.parent = node # P's parent : G => X
            else: # if P is root node
                node.left_child = node.parent
                node.left_child.parent = node
                node.parent = None
                

    def splay(self, node):
        """ 
        This method splays the nodes.
    
        Args:
            node (Node) : The node to splay.
    
        Returns:
            None
        
        """
        ### CODE HERE ###
        while node.parent != None:  # Repeat until node is root
            if node.parent == self.root: # Zig step
                self.rotate(node)
            elif node.is_left_child() and node.parent.is_left_child(): # Zig-Zig step (left)
                self.rotate(node.parent) # rotate P
                self.rotate(node) # rotate X
            elif node.is_right_child() and node.parent.is_right_child(): # Zig-Zig step (right)
                self.rotate(node.parent) # rotate P
                self.rotate(node) # rotate X
            else: # Zig-Zag step => rotate X twice
                self.rotate(node)
                self.rotate(node)
        self.root = node
        #################
    
    def insert(self, key):
        """ 
        This method inserts the key value to splay tree.
    
        Args:
            key : The key value to insert
    
        Returns:
            None
        
        """
        ### CODE HERE ###
        if self.root: # if root exists
            self._insert(key, self.root) # insert
        else: # if root doesn't exist
            self.root = Node(key) # insert the node as root
        #################

    def _insert(self, key, current):
        if key < current.key: # if key is smaller than current's key move to left child
            if current.has_left_child(): # if there is already one
                self._insert(key, current.left_child) # move down
            else: # if there is a space insert the node
                current.left_child = Node(key, parent=current) # insert the node
                self.splay(current.left_child) # splay the node
        else: # if key is same or bigger than current's key move to right child
            if current.has_right_child(): # if there is already one
                self._insert(key, current.right_child) # move down
            else: # if there is a space insert the node
                current.right_child = Node(key, parent = current) # insert the node
                self.splay(current.right_child) # splay the node


    def find(self, key):
        """ 
        This method finds the node have the specified key.
    
        Args:
            key : The key value to find.
    
        Returns:
            Bool
        
        """
        ### CODE HERE ###
        if self.root: # if root exists find from next level
            return self._find(key, self.root)
        else: # if not return false
            return False
        #################

    def _find(self, key, current):
        if current.key == key: # found => splay and return True
            self.splay(current)
            return True
        elif key < current.key: # if smaller go to left child
            if current.has_left_child():
                return self._find(key, current.left_child)
            else: # if not found => splay and return False
                self.splay(current)
                return False
        else: # else, go to right child
            if current.has_right_child():
                return self._find(key, current.right_child)
            else: # if not found => splay and return False
                self.splay(current)
                return False
        

    def delete(self, key):
        """ 
        This method delete the node has the specified key.
    
        Args:
            key : The key value to delete.
    
        Returns:
            None
        
        """
        ### CODE HERE ###
        found = self.find(key)
        if found:
            if self.root.has_both_children(): # if root has both children
                succ = self.find_max() # find the max value of left tree
                temp = self.root.right_child # back up the right child
                self.root = None # delete the root
                self.splay(succ) # splay the succ value
                self.root.right_child = temp # make right child root's right child
                self.root.right_child.parent = self.root # make right child's parent root node
            elif self.root.has_any_children(): # if root has one child
                if self.root.has_left_child(): # if root has left child
                    temp = self.root.left_child # back up the left child
                    self.root = None # delete the node
                    self.root = temp # make left child => root
                    self.root.parent = None # delete parent
                else: # if root has right child
                    temp = self.root.right_child # back up the right child
                    self.root = None # delete the node
                    self.root = temp # make right child => root
                    self.root.parent = None # delete parent
            else: # if root has no child
                self.root = None # delete the root
        else: # not found
            raise KeyError('key is not in the tree')
        #################

    def find_max(self): # used for choosing successor - biggest in left child
        current = self.root.left_child # starts with root's left child
        while current.has_right_child(): # find the last right child
            current = current.right_child
        return current # return the current node
    

    def pre_order(self, node=None):
        """ 
        Do a preorder traversal.
    
        Args:
            node : The target node.
    
        Returns:
            None
        
        """
        ### CODE HERE ###
        if node != None:
            print(node.key) # parent first
            self.pre_order(node.left_child) # left second
            self.pre_order(node.right_child) # right last
        #################
    
    def post_order(self, node=None):
        """ 
        Do a postorder traversal.
    
        Args:
            node : The target node.
    
        Returns:
            None
        
        """
        ### CODE HERE ###
        if node != None:
            self.post_order(node.left_child) # left first
            self.post_order(node.right_child) # right second
            print(node.key) # parent last
        #################
    
    def in_order(self, node=None):
        """ 
        Do an inorder traversal.
    
        Args:
            node : The target node.
    
        Returns:
            None
        
        """
        ### CODE HERE ###
        if node != None:
            self.in_order(node.left_child) # left first
            print(node.key) # parent second
            self.in_order(node.right_child) # right last
        #################

