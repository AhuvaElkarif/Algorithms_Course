"""
Algorithms Exercise 04 - All Code Solutions
Jerusalem College - Computer Science Department
Advanced Algorithms Course, Semester A 2025-2026

Student: [Your Name]
Date: January 2026
"""

# ============================================================================
# QUESTION 2: Quick Select Implementation
# ============================================================================

def quick_kth(arr, left, right, k, key=lambda x: x):
    """
    Find the k-th smallest element in arr[left:right+1] using QuickSelect algorithm.
    
    Parameters:
    - arr: the array to search in
    - left: left boundary of the subarray
    - right: right boundary of the subarray
    - k: the order statistic to find (0-indexed, so k=0 means smallest element)
    - key: function to extract comparison key from each element
    
    Returns:
    - The k-th smallest element
    """
    if left == right:  # Only one element
        return arr[left]
    
    # Partition the array and get the pivot index
    pivot_index = partition(arr, left, right, key)
    
    # The pivot is now at its final sorted position
    # Check if it's the element we're looking for
    if k == pivot_index:
        return arr[k]
    elif k < pivot_index:
        # The k-th element is in the left partition
        return quick_kth(arr, left, pivot_index - 1, k, key)
    else:
        # The k-th element is in the right partition
        return quick_kth(arr, pivot_index + 1, right, k, key)


def partition(arr, left, right, key=lambda x: x):
    """
    Lomuto partition scheme.
    Partitions arr[left:right+1] around a pivot (last element).
    
    Returns the final position of the pivot.
    All elements smaller than pivot are to its left,
    all elements greater are to its right.
    """
    # Choose the last element as pivot
    pivot = key(arr[right])
    
    # Index of smaller element, indicates the position
    # where the next smaller element should be placed
    i = left - 1
    
    for j in range(left, right):
        # If current element is smaller than or equal to pivot
        if key(arr[j]) <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    # Place pivot in its correct position
    arr[i + 1], arr[right] = arr[right], arr[i + 1]
    return i + 1


# Test cases for Question 2
def test_quick_kth():
    print("=" * 70)
    print("QUESTION 2: Quick Select Tests")
    print("=" * 70)
    
    # Test 1: Simple array
    arr1 = [3, 2, 1, 5, 4]
    print("\nTest 1: Find median (k=2) in", arr1)
    result1 = quick_kth(arr1.copy(), 0, len(arr1) - 1, 2)
    print(f"Result: {result1}")  # Should be 3
    
    # Test 2: With key function (finding by second element in tuples)
    arr2 = [('a', 5), ('b', 2), ('c', 8), ('d', 1), ('e', 6)]
    print("\nTest 2: Find 2nd smallest by value in", arr2)
    result2 = quick_kth(arr2.copy(), 0, len(arr2) - 1, 1, key=lambda x: x[1])
    print(f"Result: {result2}")  # Should be ('b', 2)
    
    # Test 3: Find minimum
    arr3 = [7, 3, 9, 1, 5]
    print("\nTest 3: Find minimum in", arr3)
    result3 = quick_kth(arr3.copy(), 0, len(arr3) - 1, 0)
    print(f"Result: {result3}")  # Should be 1
    
    # Test 4: Find maximum
    print("\nTest 4: Find maximum in", arr3)
    result4 = quick_kth(arr3.copy(), 0, len(arr3) - 1, len(arr3) - 1)
    print(f"Result: {result4}")  # Should be 9


# ============================================================================
# QUESTION 4: Binary Search Tree with Key Function
# ============================================================================

class Node:
    """Node in a binary search tree"""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class Tree:
    """Binary Search Tree with custom key function"""
    def __init__(self, key=lambda x: x):
        """
        Initialize the tree.
        
        Parameters:
        - key: function to extract the comparison key from each value
        """
        self.root = None
        self.key = key
    
    def insert(self, value):
        """
        Insert a value into the binary search tree.
        
        Parameters:
        - value: the value to insert
        """
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node, value):
        """
        Recursively insert a value into the tree.
        
        Parameters:
        - node: current node in the recursion
        - value: the value to insert
        """
        # Compare using the key function
        if self.key(value) < self.key(node.value):
            # Go to left subtree
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            # Go to right subtree (includes equal values)
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert_recursive(node.right, value)
    
    def search(self, value):
        """
        Search for a value in the tree.
        
        Parameters:
        - value: the value to search for
        
        Returns:
        - The node containing the value, or None if not found
        """
        return self._search_recursive(self.root, value)
    
    def _search_recursive(self, node, value):
        """
        Recursively search for a value.
        
        Parameters:
        - node: current node in the recursion
        - value: the value to search for
        
        Returns:
        - The node containing the value, or None if not found
        """
        if node is None:
            return None
        
        # Compare using the key function
        if self.key(value) == self.key(node.value):
            return node
        elif self.key(value) < self.key(node.value):
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)
    
    def inorder_traversal(self):
        """
        Perform inorder traversal of the tree.
        
        Returns:
        - List of values in sorted order
        """
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node, result):
        """Helper function for inorder traversal"""
        if node is not None:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)
    
    # BONUS QUESTION 5: Mermaid export functionality
    def to_mermaid(self):
        """
        Convert the tree to Mermaid diagram format.
        
        Returns:
        - String containing Mermaid diagram code
        """
        if self.root is None:
            return "graph TD\n    empty[Empty Tree]"
        
        lines = ["graph TD"]
        
        # Print root
        lines.append(f"    t(({self.root.value}))")
        
        # Recursively process the tree
        self._mermaid_recursive(self.root, "t", lines)
        
        return "\n".join(lines)
    
    def _mermaid_recursive(self, node, node_id, lines):
        """
        Recursively generate Mermaid code for the tree.
        
        Parameters:
        - node: current node
        - node_id: string identifier for the current node
        - lines: list to append Mermaid lines to
        """
        if node is None:
            return
        
        # Process left child
        if node.left is not None:
            left_id = node_id + "l"
            lines.append(f"    {node_id} --> {left_id}(({node.left.value}))")
            self._mermaid_recursive(node.left, left_id, lines)
        elif node.right is not None:
            # Add empty node if left is missing but right exists
            left_id = node_id + "l"
            lines.append(f"    {node_id} ~~~ {left_id}(( ))")
            lines.append(f"    style {left_id} fill:#fff,stroke-width:0px")
        
        # Process right child
        if node.right is not None:
            right_id = node_id + "r"
            lines.append(f"    {node_id} --> {right_id}(({node.right.value}))")
            self._mermaid_recursive(node.right, right_id, lines)
        elif node.left is not None:
            # Add empty node if right is missing but left exists
            right_id = node_id + "r"
            lines.append(f"    {node_id} ~~~ {right_id}(( ))")
            lines.append(f"    style {right_id} fill:#fff,stroke-width:0px")


# Test cases for Question 4
def test_bst_with_key():
    print("\n" + "=" * 70)
    print("QUESTION 4: Binary Search Tree with Key Function Tests")
    print("=" * 70)
    
    # Test 1: Simple tree with integers
    print("\nTest 1: Simple integer tree")
    tree1 = Tree()
    values = [10, 5, 15, 3, 7, 12, 17]
    for val in values:
        tree1.insert(val)
    print(f"Inorder traversal: {tree1.inorder_traversal()}")
    # Should print: [3, 5, 7, 10, 12, 15, 17]
    
    # Test 2: Tree with tuples, sorted by second element
    print("\nTest 2: Tree with tuples, sorted by second element")
    tree2 = Tree(key=lambda x: x[1])
    tuples = [('apple', 5), ('banana', 2), ('cherry', 8), ('date', 1)]
    for t in tuples:
        tree2.insert(t)
    print(f"Inorder traversal: {tree2.inorder_traversal()}")
    # Should print sorted by second element: [('date', 1), ('banana', 2), ('apple', 5), ('cherry', 8)]
    
    # Test 3: Tree with dictionaries, sorted by 'age' key
    print("\nTest 3: Tree with dictionaries, sorted by age")
    tree3 = Tree(key=lambda x: x['age'])
    people = [
        {'name': 'Alice', 'age': 30},
        {'name': 'Bob', 'age': 25},
        {'name': 'Charlie', 'age': 35},
        {'name': 'David', 'age': 20}
    ]
    for person in people:
        tree3.insert(person)
    print("Inorder traversal:")
    for person in tree3.inorder_traversal():
        print(f"  {person['name']}: {person['age']}")
    # Should print sorted by age: David(20), Bob(25), Alice(30), Charlie(35)
    
    # Test 4: Search functionality
    print("\nTest 4: Search in integer tree")
    found = tree1.search(7)
    if found:
        print(f"Found value: {found.value}")
    
    not_found = tree1.search(100)
    print(f"Search for 100: {'Found' if not_found else 'Not found'}")


# Test cases for Bonus Question 5
def test_mermaid_export():
    print("\n" + "=" * 70)
    print("BONUS QUESTION 5: Mermaid Export Tests")
    print("=" * 70)
    
    # Test 1: Create the tree from the example
    print("\nTest 1: Tree from the exercise example")
    tree1 = Tree()
    values = [10, 2, 16, 4, 15, 17, 20]
    for val in values:
        tree1.insert(val)
    
    mermaid_code = tree1.to_mermaid()
    print(mermaid_code)
    print("\nCopy this code to: https://www.mermaidonline.live/mermaid-to-svg")
    print("=" * 70)
    
    # Test 2: Simpler tree
    print("\nTest 2: Simple balanced tree")
    tree2 = Tree()
    values2 = [50, 30, 70, 20, 40, 60, 80]
    for val in values2:
        tree2.insert(val)
    
    print(tree2.to_mermaid())
    print("=" * 70)
    
    # Test 3: Skewed tree (left)
    print("\nTest 3: Left-skewed tree")
    tree3 = Tree()
    values3 = [5, 4, 3, 2, 1]
    for val in values3:
        tree3.insert(val)
    
    print(tree3.to_mermaid())
    print("=" * 70)
    
    # Test 4: Skewed tree (right)
    print("\nTest 4: Right-skewed tree")
    tree4 = Tree()
    values4 = [1, 2, 3, 4, 5]
    for val in values4:
        tree4.insert(val)
    
    print(tree4.to_mermaid())


# ============================================================================
# MAIN: Run all tests
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("ALGORITHMS EXERCISE 04 - ALL CODE SOLUTIONS")
    print("=" * 70)
    
    # Run all test functions
    test_quick_kth()
    test_bst_with_key()
    test_mermaid_export()
    
    print("\n" + "=" * 70)
    print("ALL TESTS COMPLETED")
    print("=" * 70)