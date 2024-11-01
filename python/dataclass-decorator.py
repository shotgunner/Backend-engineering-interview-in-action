from dataclasses import dataclass, field, InitVar, KW_ONLY, FrozenInstanceError
from typing import Any

# Basic dataclass example
@dataclass
class Person:
    name: str
    age: int = 0  # Default value
    
# Frozen dataclass (immutable)
@dataclass(frozen=True) 
class ImmutablePoint:
    x: float
    y: float

# show how is immutable
# p = ImmutablePoint(x=1, y=2)
# p.x = 3

# equivalent ImmutablePoint class without dataclass
class ImmutablePoint2:
    def __init__(self, x: float, y: float):
        # Use private backing fields
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
        
    @x.setter
    def x(self, value):
        raise FrozenInstanceError("cannot assign to field 'x'")
        
    @y.setter 
    def y(self, value):
        raise FrozenInstanceError("cannot assign to field 'y'")

    def __str__(self):
        return f"ImmutablePoint(x={self.x}, y={self.y})"
    
# p = ImmutablePoint2(x=1, y=2)
# p.x = 3  # This will now raise FrozenInstanceError

# Using post_init
# Using dataclass provides a more concise way to create classes with automatic __init__, 
# __repr__, __eq__ methods and more. Compare the two implementations below:
@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)  # Calculated field
    
    def __post_init__(self):
        self.area = self.width * self.height

x = Rectangle(width=10, height=20)
y = Rectangle(width=10, height=20)
print(x == y)

# Traditional class requires more boilerplate code and manual implementation
# of special methods that dataclass handles automatically
class Rectangle2:
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
        self.area = self.width * self.height

a = Rectangle(width=10, height=20)
b = Rectangle(width=10, height=20)
print(a == b)
print(a.area)

# Inheritance example        
@dataclass
class Vehicle:
    brand: str
    model: str
    
@dataclass
class Car(Vehicle):
    doors: int = 4

vehicle = Vehicle(brand="Toyota", model="Camry")
print(vehicle)

car = Car(brand="Toyota", model="Camry")
print(car)

# Using InitVar for initialization-only variables
@dataclass 
class Database:
    path: str
    connection: Any = field(init=False)
    debug: InitVar[bool] = False
    
    def __post_init__(self, debug):
        self.connection = f"Connected to {self.path}"
        if debug:
            print(self.connection)

# Keyword-only fields example
@dataclass
class Point3D:
    x: float
    y: float
    _: KW_ONLY
    z: float  # Must be passed as keyword arg

# Field with default_factory (mutable default)
@dataclass
class ShoppingCart:
    items: list = field(default_factory=list)
    
# Example usage:
if __name__ == "__main__":
    # Basic usage
    person = Person("Alice", 30)
    
    # Frozen class - will raise FrozenInstanceError if modified
    point = ImmutablePoint(1.0, 2.0)
    
    # Post init calculation
    rect = Rectangle(10, 20)
    print(f"Area: {rect.area}")  # Area: 200
    
    # Inheritance
    car = Car("Toyota", "Camry", 4)
    
    # InitVar usage
    db = Database("path/to/db", debug=True)
    
    # Keyword-only field
    p3d = Point3D(1.0, 2.0, z=3.0)  # z must be keyword arg
    
    # Mutable default with default_factory
    cart = ShoppingCart()
    cart.items.append("item1")
