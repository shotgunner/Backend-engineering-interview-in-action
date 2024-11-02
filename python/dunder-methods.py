# Common Python Dunder (Double Underscore) Methods

class DunderExample:
    def __init__(self, value):
        """Constructor method, called when object is instantiated"""
        self.value = value

    def __str__(self):
        """String representation for end users"""
        return f"DunderExample with value: {self.value}"

    def __repr__(self):
        """String representation for developers/debugging"""
        return f"DunderExample(value={self.value!r})"

    def __len__(self):
        """Makes object work with len()"""
        return len(str(self.value))

    def __eq__(self, other):
        """Equality comparison (==)"""
        if not isinstance(other, DunderExample):
            return NotImplemented
        return self.value == other.value

    def __lt__(self, other):
        """Less than comparison (<)"""
        if not isinstance(other, DunderExample):
            return NotImplemented
        return self.value < other.value

    def __getitem__(self, key):
        """Makes object subscriptable (obj[key])"""
        return f"Access to {key} in {self.value}"

    def __call__(self):
        """Makes object callable like a function"""
        return f"Called with value {self.value}"

    def __enter__(self):
        """Context manager entry point"""
        print("Entering context")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Context manager exit point"""
        print("Exiting context")

    def __add__(self, other):
        """Addition operator (+)"""
        if not isinstance(other, DunderExample):
            return NotImplemented
        return DunderExample(self.value + other.value)

    def __iter__(self):
        """Makes object iterable"""
        self._iter_index = 0
        return self

    def __next__(self):
        """Iterator protocol"""
        if self._iter_index >= len(str(self.value)):
            raise StopIteration
        result = str(self.value)[self._iter_index]
        self._iter_index += 1
        return result


# Example usage:
if __name__ == "__main__":
    # Basic initialization and string representation
    obj = DunderExample("test")
    print(str(obj))  # Uses __str__
    print(repr(obj))  # Uses __repr__
    
    # Length and comparison
    print(len(obj))  # Uses __len__
    obj2 = DunderExample("test")
    print(obj == obj2)  # Uses __eq__
    
    # Indexing and calling
    print(obj["key"])  # Uses __getitem__
    print(obj())  # Uses __call__
    
    # Context manager
    with DunderExample("context") as ctx:
        print("Inside context manager")
    
    # Iterator
    for char in DunderExample("iterate"):
        print(char)
