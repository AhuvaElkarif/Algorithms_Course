import random
import string

# For Python < 3.10 compatibility
try:
    from itertools import pairwise
except ImportError:
    def pairwise(iterable):
        """
        Return successive overlapping pairs taken from the input iterable.
        Equivalent to itertools.pairwise (available in Python 3.10+)
        """
        iterator = iter(iterable)
        try:
            prev = next(iterator)
        except StopIteration:
            return
        for item in iterator:
            yield prev, item
            prev = item

# ===============================
# Helper function - create_random_tuples
# ===============================
def create_random_tuples(n, k, types=None):
    """
    Create a list of n tuples, each containing k random elements of specified types.
    Parameters:
    n (int): Number of tuples to create.
    k (int): Number of elements in each tuple.
    types (list): List of types for each element in the tuple. Length must be k.
    Returns:
    list: A list of n tuples with random elements.
    """
    if types is None:
        types = [int] * k  # Default to int if no types provided
    if len(types) != k:
        raise ValueError("Length of types must be equal to k")
    
    def random_element(t):
        if t == int:
            return random.randint(0, 1000)
        elif t == float:
            return random.uniform(0.0, 1000.0)
        elif t == str:
            return ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        else:
            raise ValueError(f"Unsupported type: {t}")
    
    result = []
    for _ in range(n):
        tuple_elements = tuple(random_element(t) for t in types)
        result.append(tuple_elements)
    return result


# ===============================
# Question 1 - Sorting by different components
# ===============================
def question_1():
    """
    Creates a list of tuples and sorts it 3 times, each time by a different component
    """
    print("=== Question 1 ===\n")
    
    # Create list of tuples
    tuples_list = create_random_tuples(5, 3, [int, float, str])
    
    print("Original list:")
    for t in tuples_list:
        print(t)
    
    # Sort by first component (int)
    print("\nSorted by first component (int):")
    sorted_by_first = sorted(tuples_list, key=lambda x: x[0])
    for t in sorted_by_first:
        print(t)
    
    # Sort by second component (float)
    print("\nSorted by second component (float):")
    sorted_by_second = sorted(tuples_list, key=lambda x: x[1])
    for t in sorted_by_second:
        print(t)
    
    # Sort by third component (str)
    print("\nSorted by third component (str):")
    sorted_by_third = sorted(tuples_list, key=lambda x: x[2])
    for t in sorted_by_third:
        print(t)


# ===============================
# Question 2 - Merge and is_sorted
# ===============================
def is_sorted(a, key=lambda x: x):
    """
    Checks if a list is sorted in ascending order
    
    Args:
        a: The list to check
        key: Function that returns the key of each item
    
    Returns:
        True if the list is sorted, False otherwise
    """
    if len(a) <= 1:
        return True
    
    # Use pairwise to check each adjacent pair
    for current, next_item in pairwise(a):
        if key(current) > key(next_item):
            return False
    return True


def merge(a, b, key=lambda x: x):
    """
    Merges two sorted arrays
    
    Args:
        a: First sorted list
        b: Second sorted list
        key: Function that returns the key of each item
    
    Returns:
        Merged sorted list, or None if one of the arrays is not sorted
    """
    # Check that the arrays are sorted
    if not is_sorted(a, key) or not is_sorted(b, key):
        return None
    
    result = []
    i, j = 0, 0
    
    # Merge the two arrays
    while i < len(a) and j < len(b):
        if key(a[i]) <= key(b[j]):
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    
    # Add remaining elements
    result.extend(a[i:])
    result.extend(b[j:])
    
    return result


def question_2():
    """
    Testing merge and is_sorted functions
    """
    print("\n\n=== Question 2 ===\n")
    
    # Create two sorted lists
    list1 = [(1, 'a'), (3, 'b'), (5, 'c'), (7, 'd')]
    list2 = [(2, 'x'), (4, 'y'), (6, 'z')]
    
    print("List 1:", list1)
    print("List 2:", list2)
    print("Is list 1 sorted?", is_sorted(list1, key=lambda x: x[0]))
    print("Is list 2 sorted?", is_sorted(list2, key=lambda x: x[0]))
    
    # Merge
    merged = merge(list1, list2, key=lambda x: x[0])
    print("\nMerged list:", merged)
    
    # Test with unsorted list
    unsorted_list = [(5, 'a'), (2, 'b'), (8, 'c')]
    print("\n\nUnsorted list:", unsorted_list)
    print("Is sorted?", is_sorted(unsorted_list, key=lambda x: x[0]))
    result = merge(list1, unsorted_list, key=lambda x: x[0])
    print("Merge result with unsorted list:", result)


# ===============================
# Question 3 - Merging multiple lists
# ===============================
def merge_sorted_lists(lists, key=lambda x: x):
    """
    Merges multiple sorted lists
    
    Args:
        lists: List of sorted lists
        key: Function that returns the key of each item
    
    Returns:
        Merged sorted list
    """
    if not lists:
        return []
    
    if len(lists) == 1:
        return lists[0]
    
    # Merge using Divide & Conquer approach
    # Divide the lists into two groups and merge recursively
    mid = len(lists) // 2
    left = merge_sorted_lists(lists[:mid], key)
    right = merge_sorted_lists(lists[mid:], key)
    
    return merge(left, right, key)


def question_3():
    """
    Testing merge of multiple lists and complexity analysis
    """
    print("\n\n=== Question 3 ===\n")
    
    lists = [
        [1, 5, 9, 13],
        [2, 6, 10, 14],
        [3, 7, 11, 15],
        [4, 8, 12, 16]
    ]
    
    print("Original lists:")
    for i, lst in enumerate(lists):
        print(f"  List {i+1}: {lst}")
    
    merged = merge_sorted_lists(lists)
    print("\nMerged list:", merged)
    
    print("\n--- Complexity Analysis (Question 3b) ---")
    print("If there are k lists, each with n items:")
    print("\nOur implementation (Divide & Conquer):")
    print("  • Complexity: O(kn·log(k))")
    print("  • Recursion depth: log(k)")
    print("  • At each level: merging all kn elements")
    print("\nExplanation:")
    print("  - There are log(k) levels in the recursion")
    print("  - At each level we merge all kn elements")
    print("  - Therefore, the total complexity is O(kn·log(k))")


# ===============================
# Question 4 - Partition (Lomuto & Hoare)
# ===============================
def partition_lomuto(a, key=lambda x: x):
    """
    Performs partition using Lomuto's method
    Uses the last element as pivot
    
    Args:
        a: List to partition (modified in-place)
        key: Function that returns the key of each item
    
    Returns:
        The final index of the pivot
    """
    if len(a) <= 1:
        return 0
    
    pivot_index = len(a) - 1
    pivot_value = key(a[pivot_index])
    i = -1  # Index of the last element smaller than pivot
    
    for j in range(len(a) - 1):
        if key(a[j]) <= pivot_value:
            i += 1
            a[i], a[j] = a[j], a[i]
    
    # Move pivot to its final position
    i += 1
    a[i], a[pivot_index] = a[pivot_index], a[i]
    
    return i


def partition_hoare(a, key=lambda x: x):
    """
    Performs partition using Hoare's method
    Uses the first element as pivot
    
    Args:
        a: List to partition (modified in-place)
        key: Function that returns the key of each item
    
    Returns:
        Index of the first item greater than pivot
    """
    if len(a) <= 1:
        return 0
    
    pivot_value = key(a[0])
    i = -1
    j = len(a)
    
    while True:
        # Find element from left that is greater than pivot
        i += 1
        while i < len(a) and key(a[i]) < pivot_value:
            i += 1
        
        # Find element from right that is smaller than pivot
        j -= 1
        while j >= 0 and key(a[j]) > pivot_value:
            j -= 1
        
        # If pointers crossed, we're done
        if i >= j:
            return j + 1
        
        # Swap
        a[i], a[j] = a[j], a[i]


def question_4():
    """
    Testing partition using Lomuto and Hoare methods
    """
    print("\n\n=== Question 4 ===\n")
    
    # Test Lomuto
    print("--- Question 4a: Partition Lomuto ---")
    arr1 = [3, 7, 1, 9, 2, 5, 8, 4, 6]
    print("Original array:", arr1)
    pivot_pos = partition_lomuto(arr1)
    print("After partition (Lomuto):", arr1)
    print(f"Pivot position: {pivot_pos}, value: {arr1[pivot_pos]}")
    
    # Test Hoare
    print("\n--- Question 4b: Partition Hoare ---")
    arr2 = [3, 7, 1, 9, 2, 5, 8, 4, 6]
    print("Original array:", arr2)
    pivot_pos = partition_hoare(arr2)
    print("After partition (Hoare):", arr2)
    print(f"Partition position: {pivot_pos}")
    
    print("\n--- Question 4c: Difference between the two functions ---")
    print("Lomuto:")
    print("  • Uses the last element as pivot")
    print("  • The pivot ends up in its exact final position")
    print("  • Simpler to understand and implement")
    print("  • On average: 3n/2 swaps")
    
    print("\nHoare:")
    print("  • Uses the first element as pivot")
    print("  • The pivot is not necessarily in its final position (but in the correct region)")
    print("  • More efficient in terms of number of swaps")
    print("  • On average: n/6 fewer swaps than Lomuto")
    
    print("\n--- Question 4d: Running time ---")
    print("Running time of partition: O(n)")
    print("  • We traverse the entire array once")
    print("  • Constant number of operations per element")
    print("  • Linear complexity regardless of method (Lomuto or Hoare)")


# ===============================
# Question 5 - Partition with two pivots
# ===============================
def partition_two_pivots(a, key=lambda x: x):
    """
    Performs partition with two pivots, dividing the array into 3 segments
    
    Args:
        a: List to partition (modified in-place)
        key: Function that returns the key of each item
    
    Returns:
        tuple (p1, p2) where:
        - Elements at indices 0..p1-1 are smaller than pivot1
        - Elements at indices p1..p2-1 are between pivot1 and pivot2
        - Elements at indices p2..n-1 are greater than pivot2
    """
    if len(a) <= 1:
        return (0, len(a))
    
    # Choose two pivots from the ends
    if key(a[0]) > key(a[-1]):
        a[0], a[-1] = a[-1], a[0]
    
    pivot1 = key(a[0])
    pivot2 = key(a[-1])
    
    # i - boundary of small region (< pivot1)
    # k - boundary of large region (> pivot2)
    # j - current element being checked
    i = 1
    k = len(a) - 2
    j = 1
    
    while j <= k:
        if key(a[j]) < pivot1:
            # Belongs to small region
            a[i], a[j] = a[j], a[i]
            i += 1
            j += 1
        elif key(a[j]) > pivot2:
            # Belongs to large region
            a[j], a[k] = a[k], a[j]
            k -= 1
            # Don't advance j because we need to check the swapped element
        else:
            # Belongs to middle region
            j += 1
    
    # Move pivots to their positions
    i -= 1
    k += 1
    a[0], a[i] = a[i], a[0]
    a[-1], a[k] = a[k], a[-1]
    
    return (i, k + 1)


def question_5():
    """
    Testing partition with two pivots
    """
    print("\n\n=== Question 5 ===\n")
    print("--- Partition with Two Pivots ---\n")
    
    arr = [9, 2, 7, 1, 8, 3, 6, 4, 5, 10, 11, 0]
    print("Original array:", arr)
    
    p1, p2 = partition_two_pivots(arr)
    
    print(f"\nAfter partition with two pivots:")
    print(f"Array: {arr}")
    print(f"\nPartition:")
    print(f"  Region 1 (< pivot1): {arr[:p1]}")
    print(f"  Region 2 (between pivots): {arr[p1:p2]}")
    print(f"  Region 3 (> pivot2): {arr[p2:]}")
    print(f"\nPartition points: p1={p1}, p2={p2}")
    
    print("\n--- Advantages of Dual-Pivot Partition ---")
    print("  • Reduces recursion depth in QuickSort")
    print("  • Especially useful with many duplicate values")
    print("  • Improves average performance")
    print("  • Used in DualPivotQuickSort (Java 7+)")
    print("  • Time complexity: O(n) - same as regular partition")


# ===============================
# Running all questions
# ===============================
if __name__ == "__main__":
    question_1()
    question_2()
    question_3()
    question_4()
    question_5()
    
    print("\n" + "="*60)
    print("Finished running all exercises!")
    print("="*60)