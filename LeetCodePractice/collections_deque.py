from collections import deque

# defaultdict example - count frequencies
queue = deque([1, 2, 3])
queue.append(4)      # Add to right
print(queue)
queue.appendleft(0)  # Add to left
print(queue)
queue.pop()         # Remove from right 
print(queue)
queue.popleft()     # Remove from left
print(queue)
print(queue)

queue.extend([5, 6, 7])
print(queue)


# Implementing deque using list with python. the original python deque is more efficient. because it is implemented in C.
class FakeDeque:
    def __init__(self, lst):
        self.queue = lst

    def append(self, value):
        self.queue.append(value)

    def appendleft(self, value):
        self.queue.insert(0, value)

    def pop(self):
        if self.queue:
            return self.queue.pop()
        else:
            raise IndexError("pop from empty list")
    
    def popleft(self):
        # This implementation is slow because:
        # 1. self.queue[0] takes O(1) time but
        # 2. self.queue.remove() takes O(n) time since it needs to shift all remaining elements left
        # The real deque uses a doubly-linked list implementation in C, allowing O(1) operations at both ends
        if self.queue:
            temp = self.queue[0]
            self.queue.remove(temp)
            return temp
        else:
            raise IndexError("popleft from empty list")
        
    def extend(self, new_list):
        self.queue.extend(new_list)
    
    def __str__(self):
        return str(self.queue)
    
    def __getitem__(self, index):
        return self.queue[index]
    
    def __setitem__(self, index, value):
        self.queue[index] = value

print("test fake deque")
t = FakeDeque([1, 2, 3])
t.append(4)
print(t)
t.appendleft(0)
print(t)
t.pop()
print(t)
t.popleft()
print(t)
t.extend([5, 6, 7])
print(t)

import time
import random

# test performance of deque and fakedeque with huge number of elements with pop and popleft
nums = [random.randint(0, 1000000) for _ in range(10000000)]

start = time.time()
d = deque(nums)
for _ in range(1000000):
    d.append(random.randint(0, 1000000))

for _ in range(1000000):
    d.popleft()
end = time.time()
print(f"deque time: {end - start} seconds")

start = time.time()
d2 = FakeDeque(nums)
for _ in range(1000000):
    d2.append(random.randint(0, 1000000))

print(" we will wait now for a long time because popleft using list is slow it needs to shift all elements left it takes O(n) time a long time")
for _ in range(1000000):
    d2.popleft()  # This is slow because it shifts all elements left it takes O(n) time a long time
end = time.time()
print(f"fakedeque time: {end - start} seconds")