import unittest
import random
from .skiplist import SkipList # Assuming skiplist.py is in the same directory or accessible

class TestSkipList(unittest.TestCase):

    def setUp(self):
        # Fix the random seed for predictable tests, especially for level generation
        random.seed(42)
        self.skiplist = SkipList(max_level=8) # Use a reasonable max_level

    def test_insert_and_search_single_element(self):
        self.skiplist.insert(10)
        self.assertTrue(self.skiplist.search(10))
        self.assertFalse(self.skiplist.search(5))

    def test_insert_multiple_elements_sorted(self):
        elements = [1, 2, 3, 4, 5]
        for el in elements:
            self.skiplist.insert(el)
        for el in elements:
            self.assertTrue(self.skiplist.search(el), f"Element {el} not found")
        self.assertFalse(self.skiplist.search(0))
        self.assertFalse(self.skiplist.search(6))

    def test_insert_multiple_elements_unsorted(self):
        elements = [3, 1, 4, 5, 2]
        random.shuffle(elements) # Insert in random order
        for el in elements:
            self.skiplist.insert(el)

        # Sort elements for checking
        elements.sort()
        for el in elements:
            self.assertTrue(self.skiplist.search(el), f"Element {el} not found after unsorted insert")

        self.assertFalse(self.skiplist.search(0))
        self.assertFalse(self.skiplist.search(6))

    def test_search_non_existent_elements(self):
        self.skiplist.insert(10)
        self.skiplist.insert(20)
        self.skiplist.insert(30)
        self.assertFalse(self.skiplist.search(5))
        self.assertFalse(self.skiplist.search(15))
        self.assertFalse(self.skiplist.search(25))
        self.assertFalse(self.skiplist.search(35))

    def test_insert_duplicate_elements(self):
        # Standard skip lists typically allow duplicates or update values.
        # This implementation effectively stores duplicates if inserted.
        # Let's test searching for one of them.
        self.skiplist.insert(10)
        self.skiplist.insert(10)
        self.skiplist.insert(20)
        self.assertTrue(self.skiplist.search(10))
        # Depending on exact implementation, one might want to test count or specific node properties.
        # For this search, finding one instance is sufficient.

    def test_search_in_empty_list(self):
        self.assertFalse(self.skiplist.search(100))

    def test_large_number_of_insertions(self):
        # Reset random seed for this specific test if needed, or use the class-level one
        # random.seed(42)
        elements = list(range(100))
        random.shuffle(elements)
        for el in elements:
            self.skiplist.insert(el)

        random.shuffle(elements) # Check in random order as well
        for el in elements:
            self.assertTrue(self.skiplist.search(el), f"Element {el} not found in large list")

        self.assertFalse(self.skiplist.search(-1))
        self.assertFalse(self.skiplist.search(100))

    def test_boundary_values(self):
        self.skiplist.insert(0)
        self.assertTrue(self.skiplist.search(0))
        # Assuming skip list handles negative numbers if Node value type supports it
        self.skiplist.insert(-5)
        self.assertTrue(self.skiplist.search(-5))
        self.assertFalse(self.skiplist.search(-10))

if __name__ == '__main__':
    unittest.main()
