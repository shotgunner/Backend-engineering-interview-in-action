"""
Senior-Level Python Questions: Static Methods, Class Methods, and Related Concepts

1. What are the key differences between @staticmethod and @classmethod decorators, 
   and what are the implications for inheritance?
   
   Answer: Here's a practical example showing the difference between @staticmethod and @classmethod:

   class Date:
       def __init__(self, year, month, day):
           self.year = year
           self.month = month 
           self.day = day

       @staticmethod
       def is_valid_date(year, month, day):
           # Static method for date validation
           # Doesn't need access to class/instance
           return (1 <= month <= 12 and 
                  1 <= day <= 31 and 
                  year >= 0)

       @classmethod
       def from_string(cls, date_str):
           # Class method for alternative constructor
           # Needs cls to create new instances
           year, month, day = map(int, date_str.split('-'))
           if cls.is_valid_date(year, month, day):
               return cls(year, month, day)  # Creates instance of actual class
           raise ValueError("Invalid date")

   # Usage:
   # Static method - simple validation
   print(Date.is_valid_date(2023, 12, 25))  # True
   
   # Class method - creates new instance
   date = Date.from_string("2023-12-25")  # Creates Date instance

2. How do property decorators interact with inheritance? What happens when you override 
   a property in a child class?
   
   Answer: Properties are inherited, but can be overridden in child classes. The child class
   can override just the getter, setter, or deleter without affecting the others from parent.

3. What are descriptor protocols in Python and how do they relate to properties?
   
   Answer: Descriptors implement __get__, __set__, or __delete__ methods to customize attribute 
   access. Properties are actually implemented using descriptors under the hood.

4. When would you choose a class method over a static method for alternative constructors?
   
   Answer: Class methods are preferred for alternative constructors because they receive the 
   actual class as cls, allowing them to work properly with inheritance. Example:
   
   @classmethod
   def from_string(cls, string_data):
       # cls() will create instance of actual class, not just base class
       return cls(string_data.split(','))

5. How do static and class methods behave differently with respect to method resolution 
   order (MRO)?
   
   Answer: Class methods follow the class's MRO when looking up attributes via cls, while 
   static methods don't participate in inheritance or MRO lookups at all.

6. What are the performance implications of using properties vs direct attribute access?
   
   Answer: Properties add a small overhead as they involve descriptor protocol and function 
   calls. For simple attributes where validation isn't needed, direct access is more efficient.

7. How can you implement a read-only property that's calculated only once and cached?
   
   Answer: Combine @property with functools.cached_property:
   
   @cached_property
   def expensive_calculation(self):
       # Result is computed once and cached
       return sum(x * x for x in range(10**6))

8. What's the relationship between metaclasses and class/static methods?
   
   Answer: Metaclasses can define class methods that will be available to all instances
   of the class, while static methods defined in metaclasses are accessible only through
   the metaclass itself.
"""
