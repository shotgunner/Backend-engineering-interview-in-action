"""
Examples of different import approaches in Python
"""

# Hard imports - evaluated at parse time
import os  # Standard way to import
from pathlib import Path  # Import specific item
from collections import defaultdict as dd  # Import with alias

# Soft imports - evaluated at runtime
try:
    import optional_package
except ImportError:
    optional_package = None

# Dynamic imports using importlib
import importlib

# Basic usage - equivalent to "import math"
math = importlib.import_module('math')

# Import from package
json_lib = importlib.import_module('json')

# Import with custom error handling
def safe_import(module_name):
    try:
        return importlib.import_module(module_name)
    except ImportError:
        print(f"Could not import {module_name}")
        return None

# When to use each approach:

# 1. Hard imports (import x):
# - For required dependencies that should fail fast if missing
# - When you need the import to be visible in the module namespace
# - Most common and preferred when dependency is mandatory

# 2. Soft imports (try/except):
# - For optional features/dependencies
# - When you want to gracefully handle missing packages
# - When providing fallback behavior

# 3. Importlib:
# - When you need to import modules dynamically at runtime
# - When module names are determined programmatically
# - For plugin systems or dynamic loading
# - When you need fine-grained control over import process

# Example of conditional import with fallback
try:
    import numpy as np  # Preferred package
except ImportError:
    try:
        import array  # Fallback option
    except ImportError:
        print("Neither numpy nor array module available")

# Example of dynamic plugin loading
def load_plugin(plugin_name):
    try:
        return importlib.import_module(f'plugins.{plugin_name}')
    except ImportError:
        print(f"Plugin {plugin_name} not found")
        return None


