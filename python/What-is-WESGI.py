"""
Let's understand WSGI (Web Server Gateway Interface) with a simple story!

Imagine you're at a restaurant:
- You (the customer) are like a web browser making requests
- The waiter is like WSGI - they take your order to the kitchen and bring food back
- The kitchen is like your Python web application that prepares what you asked for

Here's how it works in code:
"""

def kitchen_chef(order):
    """This is like our Python web application - it processes requests"""
    if order == "pizza":
        return "Here's your delicious pizza! 🍕"
    elif order == "ice cream":
        return "Here's your ice cream! 🍦"
    else:
        return "Sorry, we don't have that! 😕"

def wsgi_waiter(environ, start_response):
    """
    This is our WSGI interface - like a waiter that:
    1. Takes the order (web request) from the customer
    2. Gives it to the kitchen
    3. Brings back the response
    """
    # Get what the customer ordered from their request
    path = environ.get('PATH_INFO', '').lstrip('/')
    
    # Ask the kitchen to prepare the order
    response_body = kitchen_chef(path)
    
    # Convert the response to bytes (like putting food on a plate)
    response_body = response_body.encode('utf-8')
    
    # Prepare the response headers (like getting utensils ready)
    status = '200 OK'
    response_headers = [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(response_body)))
    ]
    
    # Tell the customer their order is ready
    start_response(status, response_headers)
    
    # Deliver the food!
    return [response_body]

"""
Why do we need WSGI?
1. It's like having a standard way for waiters to work in ALL restaurants
2. Any web server can work with any Python web app because they speak the same language
3. It keeps things organized - the kitchen doesn't need to know about serving customers,
   and the waiter doesn't need to know about cooking!

To run this, you would need a WSGI server (like Gunicorn or uWSGI) that would call
our wsgi_waiter function whenever a web request comes in.

Try imagining these URLs:
http://restaurant.com/pizza -> You get a pizza! 🍕
http://restaurant.com/ice-cream -> You get ice cream! 🍦
http://restaurant.com/sushi -> Sorry message 😕
"""
