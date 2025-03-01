# Problem number 347:
# https://leetcode.com/problems/top-k-frequent-elements/description/

import collections
import heapq
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        count = collections.Counter(nums)
        freq = collections.defaultdict(list)
        for num, cnt in count.items():
            freq[cnt].append(num)
        
        result = []
        for times in range(len(nums), 0, -1):
            if times in freq:
                result.extend(freq[times])
                if len(result) >= k:
                    break
        
        return result[:k]


import collections
import heapq

def topKFrequent(nums, k):
    count = collections.Counter(nums)   
    # nlargest has a time complexity of O(n log k)
    return heapq.nlargest(k, count.keys(), key=count.get) 



def topKFrequent(nums, k):
    # Count the frequency of each number
    count = collections.Counter(nums)  
    
    # Initialize a min-heap
    heap = []
    
    # Iterate over the frequency dictionary items
    for num, freq in count.items():
        # Push the tuple (frequency, number) onto the heap
        heapq.heappush(heap, (freq, num))
        # If heap size exceeds k, pop the smallest frequency element
        if len(heap) > k:
            heapq.heappop(heap)
    
    # The heap now contains the k elements with the highest frequency.
    # We extract the numbers from the heap.
    return [num for freq, num in heap]


print(topKFrequent([1,1,1,2,2,3], 2))  # Output: [1, 2]
print(topKFrequent([1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 3, 3, 3, 2, 3, 2, 2, 2, 4, 3, 3, 3, 3, 3, 43, 4, 3], 2))  # Output: [2, 3]

# Time complexity: O(n) for counting and O(n log k) for heapq.nlargest, so O(n log k) in total.


# create max heap with heapq
heap = []

# add elements to heap
heapq.heappush(heap, (1, "a"))
heapq.heappush(heap, (2, "b"))
heapq.heappush(heap, (3, "c"))