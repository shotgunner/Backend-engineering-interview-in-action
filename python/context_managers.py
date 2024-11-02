from contextlib import contextmanager

@contextmanager
def managed_resource(resource_name):
    """A simple context manager using contextlib."""
    print(f"Acquiring resource: {resource_name}")
    try:
        yield f"Resource {resource_name} is now available"
    finally:
        print(f"Releasing resource: {resource_name}")

# Usage
if __name__ == "__main__":
    with managed_resource("Database Connection") as resource:
        print(resource) 