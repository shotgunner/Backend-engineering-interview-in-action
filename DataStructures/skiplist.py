"""
A Skip List is a probabilistic data structure that allows for efficient search,
insertion, and deletion operations, typically O(log n) on average.
It uses multiple levels of linked lists, with each level skipping over some
elements of the level below it. This structure allows for searches to "skip"
over large portions of the list, leading to logarithmic performance.

Skip lists are used in various applications where sorted data needs to be
accessed quickly, such as in databases (e.g., Redis sorted sets) and
networking. Their probabilistic nature makes their implementation simpler
than balanced trees like AVL or Red-Black trees, while offering similar
average-case performance. The worst-case performance is O(n), but this is rare.
"""

# Let's learn about Skip Lists - A fun way Redis stores sorted data!

# Time Complexity:
# - Search: O(log n) average case, O(n) worst case
# - Insert: O(log n) average case, O(n) worst case 
# - Delete: O(log n) average case, O(n) worst case

# Space Complexity: O(n) for n elements
# The number of levels affects the constant factor but not the asymptotic complexity

# Redis uses a max of 32 levels, with probability p=0.25 for level promotion
# For n elements, expected number of levels is log₁/ₚ(n)
# So with p=0.25, a million elements need ~16 levels on average

"""
Example Skip List with 4 levels (good for ~250 elements):

Level 3:   1 -----------------------> 9
Level 2:   1 --------> 5 ---------> 9  
Level 1:   1 --> 3 --> 5 --> 7 --> 9
Level 0:   1 --> 3 --> 5 --> 7 --> 9   (Base level with all elements)
"""

# Let's code a simple Skip List!
class Node:
    """
    Represents a node in the Skip List.
    Each node contains a value and a list of 'next' pointers, one for each
    level of the skip list it participates in. The height of the node (its level)
    is determined randomly during insertion.
    """
    def __init__(self, value):
        self.value = value
        # Each node can point to next nodes at different levels
        self.next = [None]  # Initialize with one slot for level 0
        self.level = 0  # Indicates the highest level this node is on (0-indexed)

class SkipList:
    """
    Implements the Skip List data structure.
    It maintains a head node and a maximum level for the list.
    Operations include insertion and search.
    The `max_level` parameter controls the maximum height a node's tower can reach.
    """
    def __init__(self, max_level=4):
        self.max_level = max_level
        # Head node is special - it's the starting point
        self.head = Node(float('-inf'))
        self.head.next = [None] * max_level
        
    def insert(self, value):
        # New node starts at level 0
        new_node = Node(value)
        current = self.head
        
        # Sometimes we make the node taller (like building floors of a tower)
        # The higher it is, the faster we can search later!
        import random
        while random.random() < 0.5 and new_node.level < self.max_level - 1:
            new_node.level += 1
            new_node.next.append(None)
            
        # Insert at each level, from top to bottom
        level = new_node.level
        while level >= 0:
            # Move right until we find the right spot
            while (current.next[level] and 
                   current.next[level].value < value):
                current = current.next[level]
                
            # Insert the new node
            new_node.next[level] = current.next[level]
            current.next[level] = new_node
            level -= 1

    def search(self, value):
        current = self.head
        # Start from the highest level
        for level in range(self.max_level - 1, -1, -1):
            # Move right while we can
            while (current.next[level] and 
                   current.next[level].value < value):
                current = current.next[level]
                
        # At bottom level, check if we found the value
        current = current.next[0]  # Move to the actual node
        return current and current.value == value

if __name__ == "__main__":
    print("--- Skip List Demonstration ---")
    # Initialize Skip List with a maximum of 5 levels
    # (Can store up to roughly 2^(5-1) = 16 elements optimally with p=0.5,
    # but can store more, just less efficiently at higher numbers)
    skiplist = SkipList(max_level=5)

    # Insert a larger set of numbers
    numbers_to_insert = [3, 6, 7, 9, 12, 19, 17, 26, 21, 25, 1, 4, 5, 8, 11]
    print(f"Inserting numbers: {numbers_to_insert}")
    for num in numbers_to_insert:
        skiplist.insert(num)
        print(f"Inserted {num}.")

    # Print the structure (simple way, level by level)
    print("\n--- Skip List Structure (Simplified) ---")
    for level in range(skiplist.max_level -1, -1, -1):
        print(f"Level {level}: Head -> ", end="")
        current = skiplist.head.next[level]
        while current:
            print(f"{current.value} -> ", end="")
            current = current.next[level]
        print("None")

    print("\n--- Search Operations ---")
    # Search for existing elements
    search_values_existing = [7, 19, 1, 25, 12]
    print(f"Searching for existing elements: {search_values_existing}")
    for val in search_values_existing:
        found = skiplist.search(val)
        print(f"Search for {val}: {'Found' if found else 'Not Found'}")

    # Search for non-existing elements
    search_values_non_existing = [10, 2, 30, 100]
    print(f"\nSearching for non-existing elements: {search_values_non_existing}")
    for val in search_values_non_existing:
        found = skiplist.search(val)
        print(f"Search for {val}: {'Found' if found else 'Not Found'}")

    print("\n--- End of Demonstration ---")

# Original comments about Redis remain valuable:
# This is how Redis uses Skip Lists for its Sorted Sets (ZSET)!
# - Each element has a score (like our numbers above)
# - Skip List makes it fast to:
#   * Find elements by score
#   * Get ranges of elements
#   * Find elements with scores between two values

# Redis uses this for:
# 1. Leaderboards (gaming scores)
# 2. Time-based data (sorted by timestamp)
# 3. Priority queues (sorted by priority)
