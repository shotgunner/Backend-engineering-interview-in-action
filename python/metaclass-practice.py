# what is a metaclass?
# a metaclass is a class of a class.
# a class is an instance of a metaclass.
# a metaclass is used to create a class.
# a metaclass is used to change a class at runtime.
# a metaclass is used to change a class at compile time.
# a metaclass is used to change a class at load time.

# examples

class MetaClass(type):
    def __new__(cls, name, bases, attrs):
        print(f"Creating class {name}")
        return super().__new__(cls, name, bases, attrs)

class MyClass(metaclass=MetaClass):
    pass

print(MyClass)

# why would we use a metaclass? here is an example:
# 1- singleton pattern

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
class MyClass(metaclass=Singleton):
    pass

print(MyClass())
print(MyClass())

# 2- something similar to django models class Meta

class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        print(f"Creating class {name}")
        return super().__new__(cls, name, bases, attrs)
    
class MyModel(metaclass=ModelMeta):
    # The Meta class is a common pattern in Django and other frameworks
    # It provides a clean namespace for configuration/metadata about the outer class
    # By nesting it inside MyModel, we:
    # 1. Keep the configuration clearly associated with its parent class
    # 2. Avoid naming conflicts with other classes' Meta configurations
    # 3. Allow the metaclass to easily find and process the configuration
    # 4. Follow the principle of encapsulation - the Meta data belongs to MyModel
    class Meta:
        db_table = "my_table"

#use db_table
print(MyModel.Meta.db_table)

