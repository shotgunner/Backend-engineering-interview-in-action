from collections import defaultdict

# defaultdict example - count frequencies

# Python defaultdict implementation but it is not as efficient as the original defaultdict. because the original defaultdict is implemented in C.
class fakedefaultdict:
    def __init__(self, class_type):
        self.d = {}
        self.class_type = class_type
    
    def __getitem__(self, key):
        # No need to print key
        if key not in self.d:
            self.d[key] = self.class_type()
        return self.d[key]

    def __setitem__(self, key, value):
        self.d[key] = value

    def __str__(self):
        return str(self.d)
    
nums = [1, 2, 2, 3, 3, 3]

freq = defaultdict(int)
for num in nums:
    freq[num] += 1
print(freq)  # defaultdict(<class 'int'>, {1: 1, 2: 2, 3: 3})

# without defaultdict
a = fakedefaultdict(int)

for i in nums:
    a[i] += 1
print(a)

import time
import random

# test performance of defaultdict and fakedefaultdict with huge number of elements
nums = [random.randint(0, 1000000) for _ in range(10000000)]

start = time.time()
freq = defaultdict(int)
for num in nums:
    freq[num] += 1
end = time.time()
print(f"defaultdict time: {end - start} seconds")

start = time.time()
a = fakedefaultdict(int)

for i in nums:
    a[i] += 1
end = time.time()
print(f"fakedefaultdict time: {end - start} seconds")