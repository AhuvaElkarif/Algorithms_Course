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
    import random
    import string

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

tuples_list = create_random_tuples(10, 3, [int, float, str])
for t in tuples_list:
    print(t)

# Question a
def find_min(a, key):
    if not a:
        raise ValueError("Empty sequence")
    min_item = max_item = a[0]
    min_key = max_key = key(a[0])
    for item in a[1:]:
        k = key(item)
        if k < min_key:
            min_key = k
            min_item = item
        if k > max_key:
            max_key = k
            max_item = item
    return min_item, max_item

if __name__ == "__main__":
    tuples_list = create_random_tuples(100, 3, [int, float, str])
    min_item, max_item = find_min(tuples_list, key=lambda x: x[2])
    print(f"min={min_item[2]}")
    print(f"max={max_item[2]}")