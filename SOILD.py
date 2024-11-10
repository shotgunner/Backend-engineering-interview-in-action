"""
SOLID Principles with Examples

1. Single Responsibility Principle (SRP)
- A class should have only one reason to change
"""

# DON'T - Class handles multiple responsibilities
class OrderProcessor:
    def process_order(self, order):
        # Handles order logic
        pass
        
    def generate_invoice(self, order):
        # Handles invoice generation
        pass
        
    def send_email(self, email):
        # Handles email sending
        pass

# DO - Split into focused classes        
class Order:
    def process(self, order):
        # Only handles order logic
        pass

class InvoiceGenerator:
    def generate(self, order):
        # Only handles invoice generation
        pass
        
class EmailService:
    def send(self, email):
        # Only handles email sending
        pass

"""
2. Open/Closed Principle (OCP) 
- Software entities should be open for extension but closed for modification
"""

# DON'T - Need to modify class to add shapes
class AreaCalculator:
    def calculate_area(self, shape_type, shape):
        if shape_type == "rectangle":
            return shape.width * shape.height
        elif shape_type == "circle":
            return 3.14 * shape.radius * shape.radius
        # Need to add more elif statements for new shapes

# DO - Use inheritance and interfaces
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def calculate_area(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
    def calculate_area(self):
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
        
    def calculate_area(self):
        return 3.14 * self.radius * self.radius

"""
3. Liskov Substitution Principle (LSP)
- Objects should be replaceable with their subtypes
"""

# DON'T - Square violates LSP for Rectangle
class Rectangle:
    def set_width(self, width):
        self._width = width
    
    def set_height(self, height):
        self._height = height

class Square(Rectangle):
    def set_width(self, width):
        self._width = width
        self._height = width  # Violates LSP
        
    def set_height(self, height):
        # This line violates LSP because it forces a Square to maintain width=height,
        # which breaks the expectation that width and height can be set independently
        # like they can in a Rectangle. This means Square is not truly substitutable
        # for Rectangle, violating Liskov Substitution Principle.
        self._width = height  # Violates LSP
        self._height = height

# DO - Use proper abstraction
class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
    def area(self):
        return self.width * self.height

class Square(Shape):
    def __init__(self, side):
        self.side = side
        
    def area(self):
        return self.side * self.side

"""
4. Interface Segregation Principle (ISP)
- Clients should not be forced to depend on interfaces they don't use
"""

# DON'T - Fat interface forces unnecessary implementation
class Worker:
    def work(self):
        pass
    
    def eat(self):
        pass
    
    def sleep(self):
        pass

# DO - Split interfaces
class Workable:
    def work(self):
        pass

class Eatable:
    def eat(self):
        pass

class Sleepable:
    def sleep(self):
        pass

class Human(Workable, Eatable, Sleepable):
    def work(self):
        print("Working")
        
    def eat(self):
        print("Eating")
        
    def sleep(self):
        print("Sleeping")

"""
5. Dependency Inversion Principle (DIP)
- High-level modules should not depend on low-level modules
- Both should depend on abstractions
"""

# DON'T - High-level module depends on low-level module
class MySQLDatabase:
    def save(self, data):
        print(f"Saving {data} to MySQL")

class UserService:
    def __init__(self):
        self.db = MySQLDatabase()  # Direct dependency
        
    def save_user(self, user):
        self.db.save(user)

# DO - Depend on abstractions
class Database(ABC):
    @abstractmethod
    def save(self, data):
        pass

class MySQLDatabase(Database):
    def save(self, data):
        print(f"Saving {data} to MySQL")

class PostgresDatabase(Database):
    def save(self, data):
        print(f"Saving {data} to Postgres")

class UserService:
    def __init__(self, database: Database):  # Dependency injection
        self.db = database
        
    def save_user(self, user):
        self.db.save(user)
