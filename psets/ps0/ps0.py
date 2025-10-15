#################
#               #
# Problem Set 0 #
#               #
#################


#
# Setup
#
class BinaryTree:
    def __init__(self, root):
        """
        :param root: the root of the binary tree
        """
        self.root: BTvertex = root
 
class BTvertex:
    def __init__(self, key):
        """
        :param: the key associated with the vertex of the binary tree
        """
        self.parent: BTvertex = None
        self.left: BTvertex = None
        self.right: BTvertex = None
        self.key: int = key
        self.size: int = None


#
# Problem 1a
#

# Input: BTvertex v, the root of a BinaryTree of size n
# Output: Up to you
# Side effect: sets the size of each vertex n in the
# ... tree rooted at vertex v to the size of that subtree
# Runtime: O(n)
def calculate_sizes(v):
    if v is None:
        return 0

    left_size = calculate_sizes(v.left)
    right_size = calculate_sizes(v.right)

    v.size = 1 + left_size + right_size

    return v.size


#
# Problem 1c
#

# Input: a positive integer t, 
# ...BTvertex v, the root of a BinaryTree of size n >= 1
# Output: BTvertex, descendent of v such that its size is between 
# ... t and 2t (inclusive)
# Runtime: O(h) 

def FindDescendantOfSize(t, v):
    def sz(node):
        return 0 if node is None else node.size

    cur = v
    while cur is not None:
        L = cur.left
        R = cur.right
        sL, sR = sz(L), sz(R)

        # If either child is in range, return it
        if L is not None and t <= sL <= 2 * t:
            return L
        if R is not None and t <= sR <= 2 * t:
            return R

        # Otherwise, follow a child whose subtree is > 2t
        if sL > 2 * t:
            cur = L
        elif sR > 2 * t:
            cur = R
        else:
            return None
