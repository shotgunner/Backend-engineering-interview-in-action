from collections import Counter, defaultdict

nums = [1, 2, 2, 3, 3, 3]

# Counter example - same as above but shorter
count = Counter(nums)
print(count)  # Counter({3: 3, 2: 2, 1: 1})

class FakeCounter:
    def __init__(self, iterable):
        self.d = {}

        # This implementation is slower than collections.Counter because:
        # 1. collections.Counter is implemented in C which is much faster than Python
        # 2. We do an explicit dictionary lookup for each item with 'if i not in self.d'
        #    whereas Counter likely uses more optimized internal C data structures
        # 3. We have two dictionary operations per item (check + set) while Counter
        #    probably does this more efficiently in one operation
        for i in iterable:
            if i not in self.d:
                self.d[i] = 0
            self.d[i] += 1
    
    def __str__(self):
        return str(self.d)
    
    def __getitem__(self, key):
        if key not in self.d:
            self.__missing__(key)
        return self.d[key]

    def __missing__(self, key):
        self.d[key] = 0
        return self.d[key]
    
a = FakeCounter(nums)
print(a)
print(a[100])

import time
import random

# test performance of Counter and FakeCounter with huge number of elements
nums = [random.randint(0, 1000000) for _ in range(20000000)]

start = time.time()
count = Counter(nums)
end = time.time()
print(f"Counter time: {end - start} seconds")

start = time.time()
a = FakeCounter(nums)
end = time.time()
print(f"FakeCounter time: {end - start} seconds")