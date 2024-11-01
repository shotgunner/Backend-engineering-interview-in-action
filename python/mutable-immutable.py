"""
Common Interview Questions About Mutable vs Immutable Types in Python
"""

# Q1: Which types in Python are immutable?
# A1: Numbers (int, float, complex), strings, tuples, frozensets
x = 5
x += 1  # Creates new object, original 5 is unchanged
print(id(5))  # Original object's id
print(id(x))  # New object's id

# Q2: Which types are mutable?
# A2: Lists, dictionaries, sets, user-defined classes
original_list = [1, 2, 3]
reference = original_list
reference.append(4)
print(original_list)  # [1, 2, 3, 4] - original is modified

# Q3: What happens when you modify a string?
# A3: A new string object is created
name = "Python"
id_before = id(name)
name += " Programming"
id_after = id(name)
print(id_before != id_after)  # True - different objects

# Q4: How do you modify a value in a tuple?
# A4: You can't modify tuple elements, but if elements are mutable, they can be modified
tuple_with_list = (1, [2, 3], 4)
# tuple_with_list[0] = 2  # TypeError
tuple_with_list[1].append(5)  # OK - modifying the list inside tuple
print(tuple_with_list)  # (1, [2, 3, 5], 4)

# Q5: How does parameter passing work with mutable/immutable types?
def modify_params(immutable_param, mutable_param):
    immutable_param += 1  # Creates new object
    mutable_param.append(4)  # Modifies original object

number = 42
my_list = [1, 2, 3]
modify_params(number, my_list)
print(number)  # 42 - unchanged
print(my_list)  # [1, 2, 3, 4] - modified

# Q6: How to create an immutable class?
from dataclasses import dataclass
@dataclass(frozen=True)
class ImmutablePoint:
    x: float
    y: float
    
point = ImmutablePoint(1.0, 2.0)
# point.x = 3.0  # FrozenInstanceError

# Q7: What's the difference between copy and deepcopy?
import copy
original = [[1, 2, 3], [4, 5, 6]]
assignment = original  # Creates a reference to the same object
shallow = copy.copy(original)  # Creates a new outer list
deep = copy.deepcopy(original)  # Creates completely new object

original[0][0] = 'X'
print(assignment[0][0])  # 'X' - assignment reference affected
print(shallow[0][0])     # 'X' - shallow copy affected
print(deep[0][0])        # 1 - deep copy unaffected

# Modifying the outer list
original.append([7, 8, 9])
print(len(assignment))  # 3 - assignment affected
print(len(shallow))     # 2 - shallow copy unaffected
print(len(deep))        # 2 - deep copy unaffected

# Q8: How to make a custom immutable container?
class ImmutableList:
    def __init__(self, items):
        self._items = tuple(items)  # Convert to immutable tuple
        
    def __getitem__(self, index):
        return self._items[index]
    
    def __len__(self):
        return len(self._items)
    
    def __str__(self):
        return str(self._items)

immutable_list = ImmutableList([1, 2, 3])
# No way to modify contents after creation
print(immutable_list[0])  # Access is allowed

# Q9: What happens in dictionary when using mutable keys?
try:
    bad_dict = {[1, 2]: "value"}  # TypeError: unhashable type: 'list'
except TypeError as e:
    print(f"Error: {e}")
    
good_dict = {(1, 2): "value"}  # OK - tuple is immutable

# Q10: How to protect class attributes from modification?
class ProtectedClass:
    def __init__(self, x):
        self._x = x
        
    @property
    def x(self):
        return self._x
    
protected = ProtectedClass(42)
print(protected.x)  # 42
# protected.x = 43  # AttributeError - can't set attribute
