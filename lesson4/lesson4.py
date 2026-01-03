# תרגיל 04 - אלגוריתמים מתקדמים
# פתרונות שאלות הקוד

"""
שאלה 2: מימוש quick_select (quick_kth)
"""

def partition(arr, left, right, key=lambda x: x):
    """
    Lomuto partition scheme with key function
    
    Args:
        arr: The array to partition
        left: Left boundary index
        right: Right boundary index
        key: Function to extract comparison key from elements
    
    Returns:
        The final index of the pivot element
    """
    pivot = key(arr[right])
    i = left - 1
    
    for j in range(left, right):
        if key(arr[j]) <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[right] = arr[right], arr[i + 1]
    return i + 1


def quick_kth(arr, left, right, k, key=lambda x: x):
    """
    Find the k-th smallest element in arr[left:right+1]
    k is 0-indexed (k=0 means smallest element)
    
    Args:
        arr: The array to search in
        left: Left boundary index
        right: Right boundary index
        k: The rank we're looking for (0-indexed)
        key: Function to extract comparison key from elements
    
    Returns:
        The k-th smallest element
    """
    if left == right:
        return arr[left]
    
    # Partition the array
    pivot_index = partition(arr, left, right, key)
    
    # The pivot is now at its final sorted position
    # Number of elements in left partition (smaller than pivot)
    num_smaller = pivot_index - left
    
    if k == num_smaller:
        # The pivot is the k-th element
        return arr[pivot_index]
    elif k < num_smaller:
        # k-th element is in the left partition
        return quick_kth(arr, left, pivot_index - 1, k, key)
    else:
        # k-th element is in the right partition
        # Adjust k relative to the right partition
        return quick_kth(arr, pivot_index + 1, right, k - num_smaller - 1, key)


# ========================================
# Tests for quick_kth
# ========================================

def test_quick_kth():
    print("="*60)
    print("Testing quick_kth function")
    print("="*60)
    
    # Test 1: Basic integer array
    print("\nTest 1: Basic integer array")
    arr1 = [3, 2, 1, 5, 4]
    print(f"Array: {arr1}")
    print(f"3rd smallest (k=2): {quick_kth(arr1.copy(), 0, len(arr1)-1, 2)}")
    print(f"Minimum (k=0): {quick_kth(arr1.copy(), 0, len(arr1)-1, 0)}")
    print(f"Maximum (k=4): {quick_kth(arr1.copy(), 0, len(arr1)-1, 4)}")
    print(f"Median (k=2): {quick_kth(arr1.copy(), 0, len(arr1)-1, len(arr1)//2)}")
    
    # Test 2: With key function - find by absolute value
    print("\nTest 2: Sort by absolute value")
    arr2 = [-5, -3, 1, 2, -4]
    print(f"Array: {arr2}")
    print(f"2nd smallest by absolute value (k=1): {quick_kth(arr2.copy(), 0, len(arr2)-1, 1, key=abs)}")
    print(f"Largest by absolute value (k=4): {quick_kth(arr2.copy(), 0, len(arr2)-1, 4, key=abs)}")
    
    # Test 3: Objects with key function
    print("\nTest 3: Objects sorted by grade")
    students = [
        {'name': 'Alice', 'grade': 85},
        {'name': 'Bob', 'grade': 92},
        {'name': 'Charlie', 'grade': 78},
        {'name': 'David', 'grade': 95}
    ]
    print(f"Students: {students}")
    median_student = quick_kth(students.copy(), 0, len(students)-1, 
                                len(students)//2, key=lambda s: s['grade'])
    print(f"Median grade student: {median_student}")
    
    # Test 4: Already sorted
    print("\nTest 4: Already sorted array")
    arr4 = [1, 2, 3, 4, 5]
    print(f"Array: {arr4}")
    print(f"Median (k=2): {quick_kth(arr4.copy(), 0, len(arr4)-1, 2)}")
    
    # Test 5: Reverse sorted
    print("\nTest 5: Reverse sorted array")
    arr5 = [5, 4, 3, 2, 1]
    print(f"Array: {arr5}")
    print(f"Median (k=2): {quick_kth(arr5.copy(), 0, len(arr5)-1, 2)}")


"""
שאלה 4: מימוש insert של עץ בינארי עם פונקציה key
"""

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class Tree:
    def __init__(self, key=lambda x: x):
        self.root = None
        self.key = key
    
    def insert(self, value):
        """Insert a value into the BST using the key function"""
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node, value):
        """Helper method for recursive insertion"""
        # Compare using the key function
        if self.key(value) < self.key(node.value):
            # Go left
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            # Go right (including equal values)
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert_recursive(node.right, value)
    
    def inorder_traversal(self, node=None, first_call=True):
        """Print tree in sorted order"""
        if first_call:
            node = self.root
        
        if node is not None:
            self.inorder_traversal(node.left, False)
            print(f"{node.value} (key={self.key(node.value)})", end=" ")
            self.inorder_traversal(node.right, False)
    
    def search(self, target_key):
        """Search for a value by its key"""
        return self._search_recursive(self.root, target_key)
    
    def _search_recursive(self, node, target_key):
        """Helper method for recursive search"""
        if node is None:
            return None
        
        if target_key == self.key(node.value):
            return node.value
        elif target_key < self.key(node.value):
            return self._search_recursive(node.left, target_key)
        else:
            return self._search_recursive(node.right, target_key)
    
    def to_mermaid(self):
        """
        שאלה 5 (בונוס): Generate Mermaid diagram representation of the tree
        """
        if self.root is None:
            return "graph TD\n    empty((empty))"
        
        lines = ["graph TD"]
        self._mermaid_recursive(self.root, "t", lines)
        return "\n".join(lines)
    
    def _mermaid_recursive(self, node, node_id, lines):
        """Helper method to recursively generate Mermaid code"""
        if node is None:
            return
        
        # Print current node
        lines.append(f"    {node_id}(({node.value}))")
        
        # Handle left child
        if node.left is not None:
            left_id = node_id + "l"
            lines.append(f"    {node_id} --> {left_id}(({node.left.value}))")
            self._mermaid_recursive(node.left, left_id, lines)
        elif node.right is not None:
            # Add empty left node only if right exists
            left_id = node_id + "l"
            lines.append(f"    {node_id} ~~~ {left_id}(( ))")
            lines.append(f"    style {left_id} fill:#fff,stroke-width:0px")
        
        # Handle right child
        if node.right is not None:
            right_id = node_id + "r"
            lines.append(f"    {node_id} --> {right_id}(({node.right.value}))")
            self._mermaid_recursive(node.right, right_id, lines)
        elif node.left is not None:
            # Add empty right node only if left exists
            right_id = node_id + "r"
            lines.append(f"    {node_id} ~~~ {right_id}(( ))")
            lines.append(f"    style {right_id} fill:#fff,stroke-width:0px")


# ========================================
# Tests for Binary Search Tree
# ========================================

def test_binary_search_tree():
    print("\n" + "="*60)
    print("Testing Binary Search Tree with Key Function")
    print("="*60)
    
    # Test 1: Simple integer tree (default key function)
    print("\nTest 1: Simple integer tree")
    tree1 = Tree()
    values = [10, 5, 15, 3, 7, 12, 17]
    print(f"Inserting values: {values}")
    for v in values:
        tree1.insert(v)
    print("Inorder traversal:", end=" ")
    tree1.inorder_traversal()
    print()
    
    # Test 2: Tree with custom key - sort by absolute value
    print("\nTest 2: Sort by absolute value")
    tree2 = Tree(key=abs)
    values = [5, -3, 10, -7, 2, -12]
    print(f"Inserting values: {values}")
    for v in values:
        tree2.insert(v)
    print("Inorder traversal:", end=" ")
    tree2.inorder_traversal()
    print()
    
    # Test 3: Tree with objects - sort by specific field
    print("\nTest 3: Objects sorted by age")
    tree3 = Tree(key=lambda p: p['age'])
    people = [
        {'name': 'Alice', 'age': 30},
        {'name': 'Bob', 'age': 25},
        {'name': 'Charlie', 'age': 35},
        {'name': 'David', 'age': 28}
    ]
    print(f"Inserting people: {[p['name'] for p in people]}")
    for person in people:
        tree3.insert(person)
    print("Inorder traversal:", end=" ")
    tree3.inorder_traversal()
    print()
    
    # Test search
    print("\nSearching for age 28:", tree3.search(28))
    print("Searching for age 40:", tree3.search(40))


def test_mermaid():
    print("\n" + "="*60)
    print("Testing Mermaid Diagram Generation (Question 5 - Bonus)")
    print("="*60)
    
    # Create the tree from the example in the question
    print("\nExample from question:")
    tree = Tree()
    values = [10, 2, 16, 4, 15, 17, 20]
    for v in values:
        tree.insert(v)
    
    print(tree.to_mermaid())
    print("\nCopy the above text to: https://www.mermaidonline.live/mermaid-to-svg")
    
    # Create another example tree
    print("\n" + "="*60)
    print("Another example tree:")
    tree2 = Tree()
    values2 = [50, 30, 70, 20, 40, 60, 80, 10, 25]
    for v in values2:
        tree2.insert(v)
    
    print(tree2.to_mermaid())
    print("\nCopy the above text to: https://www.mermaidonline.live/mermaid-to-svg")


# ========================================
# Main - Run all tests
# ========================================

if __name__ == "__main__":
    print("תרגיל 04 - בדיקות קוד")
    print("="*60)
    
    # Run all tests
    test_quick_kth()
    test_binary_search_tree()
    test_mermaid()
    
    print("\n" + "="*60)
    print("כל הבדיקות הסתיימו בהצלחה!")
    print("="*60)