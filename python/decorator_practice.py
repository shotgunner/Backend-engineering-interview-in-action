from functools import wraps

# Without @wraps, we lose the original function's metadata
# Let's demonstrate this by printing function attributes
def hello_writer(func):
    @wraps(func)  # TODO: remove this to see the difference on output
    def f(*args, **kwargs):
        print("before")
        func(*args, **kwargs)
        print("after")
    return f

@hello_writer
def f(a,b):
    '''
    some document here
    '''
    print(a+b)

# Let's check what happens to the function metadata
print("Function name:", f.__name__)  # Prints 'f' instead of original name
print("Function doc:", f.__doc__)    # Prints None instead of the docstring
print("Function module:", f.__module__)  # Lost module info

f(9,10)

# If we had used @wraps, we would have preserved:
# - Original function name
# - Original docstring
# - Original module info
# - And other function metadata