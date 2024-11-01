"""
Common itertools and functools Methods for Senior Python Engineers
"""
from itertools import (
    count, cycle, repeat,  # Infinite iterators
    chain, combinations, combinations_with_replacement,  # Combinatoric iterators
    groupby, permutations, product,  # More combinatoric iterators
    islice, tee, zip_longest  # Terminating iterators
)
from functools import (
    cache, lru_cache,  # Caching decorators
    partial, partialmethod,  # Partial function application
    reduce,  # Reduction function
    singledispatch,  # Single dispatch generic functions
    total_ordering,  # Class decorator for ordering
    wraps  # Decorator utility
)
from operator import add, mul

# Infinite Iterators Example
def infinite_iterator_example():
    # count: Count from n indefinitely
    for i in islice(count(10), 5):
        print(i)  # 10, 11, 12, 13, 14
        
    # cycle: Cycle through an iterable indefinitely
    colors = cycle(['red', 'green', 'blue'])
    print([next(colors) for _ in range(5)])  # ['red', 'green', 'blue', 'red', 'green']
    
    # repeat: Repeat an object indefinitely or n times
    for x in repeat("hello", 3):
        print(x)  # hello hello hello

# Combinatoric Iterator Examples
def combinatoric_iterator_example():
    # combinations: r-length tuples in sorted order, no repeated elements
    items = 'ABCD'
    print(list(combinations(items, 2)))  # [('A','B'), ('A','C'), ('A','D'), ('B','C'), ('B','D'), ('C','D')]
    
    # combinations_with_replacement: allows repeated elements
    print(list(combinations_with_replacement('ABC', 2)))
    
    # permutations: r-length permutations of elements
    print(list(permutations('ABC', 2)))
    
    # product: Cartesian product of input iterables
    print(list(product('AB', '12')))  # [('A','1'), ('A','2'), ('B','1'), ('B','2')]

# Functools Examples
# @cache is an unbounded cache that stores all results indefinitely
# Good for pure functions with limited input space like fibonacci
@cache  
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# @lru_cache has a max size and evicts least recently used items when full
# Better for functions with large/infinite input space to prevent memory leaks
@lru_cache(maxsize=128)  
def expensive_computation(n):
    return sum(i * i for i in range(n))

# Partial function application
def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

# Single dispatch example
@singledispatch
def process_data(data):
    raise NotImplementedError("Unsupported type")

@process_data.register(str)
def _(data):
    return f"Processing string: {data}"

@process_data.register(list)
def _(data):
    return f"Processing list with {len(data)} items"

# Total ordering example
@total_ordering
class Number:
    def __init__(self, value):
        self.value = value
        
    def __eq__(self, other):
        return self.value == other.value
        
    def __lt__(self, other):
        return self.value < other.value

# Practical Examples
def practical_examples():
    # Using reduce
    numbers = [1, 2, 3, 4, 5]
    sum_result = reduce(add, numbers)
    product_result = reduce(mul, numbers)
    print(f"Sum: {sum_result}, Product: {product_result}")
    
    # Using groupby
    data = [
        {'name': 'Alice', 'age': 25},
        {'name': 'Bob', 'age': 25},
        {'name': 'Charlie', 'age': 30}
    ]
    for age, group in groupby(data, key=lambda x: x['age']):
        print(f"Age {age}: {list(group)}")
        
    # Using chain
    lists = [[1, 2], [3, 4], [5, 6]]
    flattened = list(chain.from_iterable(lists))
    print(f"Flattened: {flattened}")

if __name__ == "__main__":
    infinite_iterator_example()
    combinatoric_iterator_example()
    practical_examples()
    
    # Test fibonacci with cache
    print(fibonacci(100))  # Very fast due to caching
    
    # Test process_data with different types
    print(process_data("Hello"))
    print(process_data([1, 2, 3]))
