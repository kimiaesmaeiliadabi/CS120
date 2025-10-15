class BinarySearchTree:
    # left: BinarySearchTree
    # right: BinarySearchTree
    # key: int
    # item: int
    # size: int
    def __init__(self, debugger = None):
        self.left = None
        self.right = None
        self.key = None
        self.item = None
        self._size = 1
        self.debugger = debugger

    @property
    def size(self):
         return self._size
       
     # a setter function
    @size.setter
    def size(self, a):
        debugger = self.debugger
        if debugger:
            debugger.inc_size_counter()
        self._size = a

    ####### Part a #######
    '''
    Calculates the size of the tree
    returns the size at a given node
    '''
    def calculate_sizes(self, debugger = None):
        # Debugging code
        # No need to modify
        # Provides counts
        if debugger is None:
            debugger = self.debugger
        if debugger:
            debugger.inc()

        # Implementation
        self.size = 1
        if self.right is not None:
            self.size += self.right.calculate_sizes(debugger)
        if self.left is not None:
            self.size += self.left.calculate_sizes(debugger)
        return self.size

    '''
    Select the ind-th key in the tree
    
    ind: a number between 0 and n-1 (the number of nodes/objects)
    returns BinarySearchTree/Node or None
    '''
    def select(self, ind):
        # size of left subtree
        left_size = self.left.size if self.left is not None else 0

        if ind == left_size:
            return self
        if ind < left_size:
            return self.left.select(ind) if self.left is not None else None
        # ind > left_size: skip left subtree and current node
        if self.right is not None:
            return self.right.select(ind - left_size - 1)
        return None


    '''
    Searches for a given key
    returns a pointer to the object with target key or None (Roughgarden)
    '''
    def search(self, key):
        if self is None:
            return None
        elif self.key == key:
            return self
        elif self.key < key and self.right is not None:
            return self.right.search(key)
        elif self.left is not None:
            return self.left.search(key)
        return None
    

    '''
    Inserts a key into the tree
    key: the key for the new node; 
        ... this is NOT a BinarySearchTree/Node, the function creates one
    
    returns the original (top level) tree - allows for easy chaining in tests
    '''
    def insert(self, key):
        if self.key is None:
        # inserting into an empty node
            self.key = key
            self.size = 1  # subtree of a single node
            return self

        if key < self.key:
            if self.left is None:
                self.left = BinarySearchTree(self.debugger)
            self.left.insert(key)
        elif key > self.key:
            if self.right is None:
                self.right = BinarySearchTree(self.debugger)
            self.right.insert(key)
        else:
            # keys are distinct
            # but if equal, do nothing
            return self

        # O(1) size maintenance from children (no full recompute)
        left_sz  = self.left.size  if self.left  is not None else 0
        right_sz = self.right.size if self.right is not None else 0
        self.size = 1 + left_sz + right_sz
        return self

    
    ####### Part b #######

    '''
    Performs a `direction`-rotate the `side`-child of (the root of) T (self)
    direction: "L" or "R" to indicate the rotation direction
    child_side: "L" or "R" which child of T to perform the rotate on
    Returns: the root of the tree/subtree
    Example:
    Original Graph
      10
       \
        11
          \
           12
    
    Execute: NodeFor10.rotate("L", "R") -> Outputs: NodeFor10
    Output Graph
      10
        \
        12
        /
       11 
    '''
    def rotate(self, direction, child_side):
        # pick which child we are rotating
        x = self.left if child_side == "L" else self.right
        if x is None:
            return self  # nothing to rotate

        # local helper for safe subtree size
        def SZ(u): 
            return 0 if u is None else u.size

        if direction == "L":
            # left-rotate at x (needs x.right)
            y = x.right
            if y is None:
                return self  # nothing to rotate

            # 1) move y.left to be x.right
            x.right = y.left

            # 2) lift y to replace x under self
            if child_side == "L":
                self.left = y
            else:
                self.right = y

            # 3) hang x as y.left
            y.left = x

            # 4) fix sizes bottom-up on the two changed nodes
            x.size = 1 + SZ(x.left) + SZ(x.right)
            y.size = 1 + SZ(y.left) + SZ(y.right)
            return self

        elif direction == "R":
            # right-rotate at x (needs x.left)
            y = x.left
            if y is None:
                return self  # nothing to rotate

            # 1) move y.right to be x.left
            x.left = y.right

            # 2) lift y to replace x under self
            if child_side == "L":
                self.left = y
            else:
                self.right = y

            # 3) hang x as y.right
            y.right = x

            # 4) fix sizes bottom-up on the two changed nodes
            x.size = 1 + SZ(x.left) + SZ(x.right)
            y.size = 1 + SZ(y.left) + SZ(y.right)
            return self

        # do nothing for unrecognized input
        return self

    def print_bst(self):
        if self.left is not None:
            self.left.print_bst()
        print( self.key),
        if self.right is not None:
            self.right.print_bst()
        return self