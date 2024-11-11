from typing import Annotated
from dataclasses import dataclass
from typing import TypeVar, Generic, Protocol, Literal, Final, TypedDict, NewType, Union, Optional, Callable, Awaitable, Any, TypeGuard, overload, ParamSpec, Concatenate, ContextManager, runtime_checkable
from abc import abstractmethod

# python doesn't care about the hints, they are only used by type checkers like mypy.
# why we need them?
# 1. to provide more information to the type checker
# 2. to provide more information to the developer
# 3. to improve the performance of the code using less debugging time wasting


# source from: https://fastapi.tiangolo.com/python-types/
# simple types
def get_items(item_a: str, item_b: int, item_c: float, item_d: bool, item_e: bytes):
    return item_a, item_b, item_c, item_d, item_d, item_e

# Generic types with type parameters¶
# There are some data structures that can contain other values, like dict, list, set and tuple. And the internal values can have their own type too.
def get_items_from_list(items: list[str]):  # in older versions of python we would use capital List instead of list
    return items  # => list of strings

def process_items(prices: dict[str, float]):
    for item_name, item_price in prices.items():
        print(item_name)
        print(item_price)

# Union types
def process_item(item: int | str):
    print(item)

# older versions of python for using Union
from typing import Union
def process_item(item: Union[int, str]):
    print(item)


# Possibly None
from typing import Optional
def say_hi(name: Optional[str] = None):
    if name is not None:
        print(f"Hey {name}!")
    else:
        print("Hello World")

# in python 3.10+ we can use the following syntax for None
def say_hi(name: str | None = None):  # -> you don't need to Union[str, None] anymore in newer versions of python
    if name is not None:
        print(f"Hey {name}!")
    else:
        print("Hello World")

# Generic types are all above examples like list, dict, Union, Optional, etc.
# you can also use classes as types
class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

def get_user_name(user: User):
    return user.name

# Basic Annotated example with type and metadata
# UserId = Annotated[int, "User identifier in our system"]
# The above adds metadata/documentation to the type that can be accessed at runtime
# While this is equivalent for type checking:
# UserId: int  # This is just a type hint that gets erased at runtime
UserId = Annotated[int, "User identifier in our system"]
Age = Annotated[int, "Age must be between 0 and 150"]


# Example with multiple metadata
Coordinate = Annotated[float, "Geographic coordinate", "Must be between -180 and 180"]

# Using Annotated with dataclass
# Advantages of dataclass:
# - Automatically generates __init__, __repr__, __eq__ methods
# - Less boilerplate code, more concise and readable
# - Built-in support for frozen (immutable) instances
# - Easier to maintain as fields are clearly defined at class level
@dataclass
class UserDataClass:
    id: UserId
    name: Annotated[str, "User's full name"]
    age: Age
    location: tuple[Coordinate, Coordinate]  # (latitude, longitude)

# Using Annotated with normal class
# Advantages of normal class:
# - More flexible and customizable
# - Full control over initialization logic
# - Can define custom methods and behaviors more naturally
# - Better when you need complex initialization or validation
class UserNormalClass:
    def __init__(self, id: UserId, name: Annotated[str, "User's full name"], 
                 age: Age, location: tuple[Coordinate, Coordinate]):  # (latitude, longitude)
        self.id = id
        self.name = name 
        self.age = age
        self.location = location

    def __eq__(self, other):
        if not isinstance(other, UserNormalClass):
            return NotImplemented
        return (self.id == other.id and 
                self.name == other.name and
                self.age == other.age and 
                self.location == other.location)

    def __repr__(self):
        return f"UserNormalClass(id={self.id}, name='{self.name}', age={self.age}, location={self.location})"

# Function using annotated types
def create_user(
    user_id: UserId,
    name: Annotated[str, "Must not be empty"],
    age: Annotated[int, "Must be positive"]
) -> UserDataClass:
    return UserDataClass(
        id=user_id,
        name=name,
        age=age,
        location=(0.0, 0.0)
    )

# Example usage
user = create_user(
    user_id=123,
    name="John Doe",
    age=30
)

# You can access metadata using typing.get_type_hints
from typing import get_type_hints
print(get_type_hints(create_user, include_extras=True))

# Python Type System Cheatsheet

# 1. Type Variables and Generics
T = TypeVar('T')  # Unbounded type variable - can be any type
S = TypeVar('S', bound=str)  # Bounded type variable - must be str or subclass of str

# Example usage:
# def first[T](x: list[T]) -> T:  # T can be ANY type
#     return x[0]

# def str_func[S](x: S) -> S:  # S must be str or subclass of str
#     return x.upper()  # Safe to call str methods

class Stack(Generic[T]):
    def push(self, item: T) -> None: ...
    def pop(self) -> T: ...

# Protocols (Structural Subtyping) more on protocols in protocol-class.py
@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> None: ...

# 3. Type Aliases
Vector = list[float]
Point = tuple[float, float]
ConnectionOptions = dict[str, str]

# 4. Literal Types
Mode = Literal['r', 'w', 'a']
def open_file(path: str, mode: Mode) -> None: ...

# 5. Final and Const
TIMEOUT: Final[int] = 60
class Config:
    DEBUG: Final = True

# 6. TypedDict
class MovieDict(TypedDict):
    title: str
    year: int
    rating: float

# 7. NewType (Creating Distinct Types)
UserId = NewType('UserId', int)
user_id = UserId(1)  # Type-safe

# 8. Union and Optional
Result = Union[str, int]  # Python 3.9: str | int
MaybeStr = Optional[str]  # Same as Union[str, None]

# 9. Callable Types
Handler = Callable[[str, int], bool]
async_handler: Callable[..., Awaitable[str]]

# 10. Type Guards
def is_string(val: Any) -> TypeGuard[str]:
    return isinstance(val, str)

# 11. Overload
@overload
def process(response: None) -> None: ...
@overload
def process(response: int) -> str: ...

# 12. ParamSpec (Python 3.10+)
P = ParamSpec('P')
def decorator(func: Callable[P, T]) -> Callable[P, T]: ...

# 13. Concatenate (Python 3.10+)
Callback = Callable[Concatenate[int, P], None]

# 14. Type Assertions
reveal_type(x)  # Only works in type checkers
assert isinstance(x, int)  # Runtime check

# 15. Abstract Base Classes
class Abstract(ABC):
    @abstractmethod
    def my_abstract_method(self) -> None: ...

# 16. Context Managers Types
class Manager(ContextManager[str]):
    def __enter__(self) -> str: ...
    def __exit__(self, *args) -> None: ...

# 17. Async Types
async def fetch_data() -> Awaitable[str]: ...
AsyncIterator[int]
AsyncIterable[str]

# 18. Collection Types
from collections.abc import (
    Sequence,
    MutableSequence,
    Mapping,
    MutableMapping,
    Set,
    MutableSet
)

# 19. Never Type (Python 3.11+)
def never_returns() -> Never:
    raise Exception("This function never returns normally")

# 20. Self Type (Python 3.11+)
class Chain:
    def next(self) -> Self:
        return self

