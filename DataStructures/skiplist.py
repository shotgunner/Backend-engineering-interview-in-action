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
    def __init__(self, value):
        self.value = value
        # Each node can point to next nodes at different levels
        self.next = []  # List of next pointers for each level
        self.level = 0  # How tall is this node's "tower"

class SkipList:
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

# Example usage:
"""
skiplist = SkipList()
skiplist.insert(3)
skiplist.insert(6)
skiplist.insert(7)
skiplist.insert(9)
skiplist.insert(12)

# When we search for 7, we can:
# 1. Start at the top level
# 2. Skip many nodes using higher levels
# 3. Only check a few nodes instead of all of them!
# This makes searching much faster than a regular list.
"""

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
