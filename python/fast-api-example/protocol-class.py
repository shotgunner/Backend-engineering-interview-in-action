from typing import runtime_checkable

# protocols (Structural Subtyping)
# Example showing how Protocols enable duck typing:

from typing import Protocol

# Define a Protocol that requires a "speak" method
@runtime_checkable
class Speakable(Protocol):
    def speak(self) -> str: ...

# These classes don't inherit from Speakable,
# but they implement the required "speak" method
class Dog:
    def speak(self) -> str:
        return "Woof!"

class Cat:
    def speak(self) -> str:
        return "Meow!"

# Function that accepts any Speakable
def make_noise(animal: Speakable) -> str:
    return animal.speak()

# Both Dog and Cat work because they match the Protocol
dog = Dog()
cat = Cat()

# Type checker allows this:
print(make_noise(dog))  # "Woof!"
print(make_noise(cat))  # "Meow!"

# Runtime checks work with @runtime_checkable:
print(isinstance(dog, Speakable))  # True
print(isinstance(cat, Speakable))  # True


# what is the diffence bettween this and ABC with example ?


from abc import ABC, abstractmethod


class Animal(ABC):
    @abstractmethod
    def walk(self) -> None:
        pass

    @abstractmethod
    def speak(self) -> None:
        pass


class Dog(Animal):
    # if we don't implement the abstract method, we will get an error
    def walk(self) -> None:
        print("This is a dog walking")

    # same here
    def speak(self) -> None:
        print("Woof!")

dog = Dog()
dog.walk()
dog.speak()

# define same classes with protocols

from typing import Protocol

@runtime_checkable  
# without above decorator, we will get an error on isinstance check why ? 
# => because protocols are only checked at type-checking time not runtime
# the steps of running the code from top to bottom is as follows:
# 1. type checking
# 2. runtime checking
# if we don't use @runtime_checkable, the protocols are only checked at type-checking time not runtime
class Animal(Protocol):
    def walk(self) -> None:
        ...

    def speak(self) -> None:
        ...

class Dog:
    def walk(self) -> None:
        print("This is a dog walking")

dog = Dog()
dog.walk()
isinstance(dog, Animal)

# Nominal typing example
# In nominal typing, types are compatible only if they have an explicit inheritance relationship
class Shape:
    def area(self) -> float:
        return 0.0

class Circle(Shape):  # Explicitly inherits from Shape
    def __init__(self, radius: float):
        self.radius = radius
    
    def area(self) -> float:
        return 3.14 * self.radius * self.radius

# This works because Circle is explicitly a subclass of Shape
def calculate_shape_area(shape: Shape) -> float:
    return shape.area()

circle = Circle(5.0)
print(calculate_shape_area(circle))  # Works fine

# Structural typing example using Protocol. duck typing in python like len() is an example of structural typing
# In structural typing, types are compatible if they have the required methods/attributes
# regardless of inheritance
@runtime_checkable
class HasArea(Protocol):
    def area(self) -> float: ...

class Rectangle:  # Note: Does NOT inherit from Shape or HasArea
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height

# This works because Rectangle has an area() method, even though it doesn't inherit from HasArea
def calculate_area(shape: HasArea) -> float:
    return shape.area()

rectangle = Rectangle(2.0, 3.0)
print(calculate_area(rectangle))  # Works fine
print(isinstance(rectangle, HasArea))  # Returns True because Rectangle has area() method. without @runtime_checkable, we will get an error

# This demonstrates how structural typing is more flexible:
# Rectangle works with calculate_area() because it has the required structure (area method)
# But it wouldn't work with calculate_shape_area() because it doesn't inherit from Shape

# summary:
# 1. nominal typing is when the name of the class is important
# 2. structural typing is when the structure of the class is important
# 3. protocols are an example of structural typing
# 4. protocols are more flexible than ABCs

