import sys
import gc
from typing import Any
import ctypes

def demonstrate_memory_management():
    """
    Demonstrates Python's memory management concepts including:
    - Reference counting
    - Garbage collection 
    - Memory allocation on heap for dynamic memory management
    """
    print("\n=== Python Memory Management Demo ===\n")

    print("1. Why Python Uses Heap Memory:")
    print("- Dynamic memory allocation: Objects can grow/shrink at runtime")
    print("- Flexible lifetime: Objects persist beyond function scope")
    print("- Reference counting: Heap allows tracking object references")
    print("- Memory sharing: Multiple references can point to same heap object")
    print("- Garbage collection: Heap memory can be reclaimed when no longer needed\n")

    # Demonstrate heap allocation benefits
    print("2. Heap Allocation Examples:")
    
    # Lists can grow dynamically
    dynamic_list = []
    print("Empty list created on heap")
    dynamic_list.append(1)
    dynamic_list.append(2)
    print(f"List grew dynamically: {dynamic_list}")

    # Objects persist beyond scope
    def create_object():
        obj = {"data": "persists"}
        return obj
    
    persistent = create_object()
    print(f"\nObject persists after function returns: {persistent}")

    # Multiple references to same object
    list1 = [1, 2, 3]
    list2 = list1  # Both reference same heap object
    list1.append(4)
    print(f"\nShared heap object modified through either reference:")
    print(f"list1: {list1}")
    print(f"list2: {list2}")

    print("\n=== Memory Layout Diagram ===")
    print("""
    Stack (Fixed Size)         Heap (Dynamic Size)
    ---------------           -------------------
    |             |          |                 |
    | References  |--------->| • Dynamic Lists |
    | Variables   |          | • Class Objects |
    | Call Frames |          | • Dictionaries  |
    |             |          | • Custom Objects|
    ---------------           -------------------
    """)

if __name__ == "__main__":
    demonstrate_memory_management()
