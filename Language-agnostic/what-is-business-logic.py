from flask import Flask, request

app = Flask(__name__)

# what is business logic? and why we should separate it from the rest of the code?

# Business logic is the part of the program that encodes the real-world business rules,
# calculations, and processes that define how data can be created, stored, and modified.

# Bad Example - Business Logic Mixed with Presentation Layer
@app.route('/create_order', methods=['POST'])
def create_order():
    # Business logic mixed directly in the route handler
    if request.form['quantity'] <= 0:
        return "Invalid quantity", 400
    
    total_price = float(request.form['quantity']) * float(request.form['unit_price'])
    if total_price > 1000:
        total_price = total_price * 0.9  # 10% discount
    
    if request.form['shipping'] == 'express':
        total_price += 25
    elif request.form['shipping'] == 'standard':
        total_price += 10
    
    # Database operations mixed with business logic
    # order = Order(
    #     quantity=request.form['quantity'],
    #     unit_price=request.form['unit_price'],
    #     total_price=total_price,
    #     shipping=request.form['shipping']
    # )
    # db.session.add(order)
    # db.session.commit()
    
    return "Order created", 201

# Good Example - Separated Business Logic
class OrderService:
    def calculate_price(self, quantity, unit_price, shipping_method):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
            
        total_price = quantity * unit_price
        
        # Business rules in a dedicated service
        if total_price > 1000:
            total_price = self.apply_bulk_discount(total_price)
            
        shipping_cost = self.calculate_shipping_cost(shipping_method)
        return total_price + shipping_cost
    
    def apply_bulk_discount(self, price):
        return price * 0.9  # 10% discount
    
    def calculate_shipping_cost(self, method):
        shipping_rates = {
            'express': 25,
            'standard': 10
        }
        return shipping_rates.get(method, 0)

@app.route('/create_order', methods=['POST'])
def create_order():
    try:
        # Route handler only deals with HTTP concerns
        order_service = OrderService()
        total_price = order_service.calculate_price(
            quantity=float(request.form['quantity']),
            unit_price=float(request.form['unit_price']),
            shipping_method=request.form['shipping']
        )
        
        # Database operations separated from business logic
        # order = Order(
        #     quantity=request.form['quantity'],
        #     unit_price=request.form['unit_price'],
        #     total_price=total_price,
        #     shipping=request.form['shipping']
        # )
        # db.session.add(order)
        # db.session.commit()
        
        return "Order created", 201
    except ValueError as e:
        return str(e), 400

# Benefits of separation:
# 1. Business logic is reusable across different interfaces (web, API, CLI)
# 2. Easier to test business rules in isolation
# 3. Changes to business rules don't affect the presentation layer
# 4. Clearer code organization and maintenance

# We can even extract the business logic hardcoded values to a separated ENV or JSON file.
