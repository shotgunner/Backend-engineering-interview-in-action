from fastapi import FastAPI, Depends, HTTPException
from typing import Optional, Callable
from dataclasses import dataclass
import logging
"""
Dependency Injection (DI) Fundamentals:

Dependency injection is a design pattern where a class/function receives its dependencies 
from external sources rather than creating them internally. This promotes:

1. Loose coupling between components
2. Easier testing through mock dependencies 
3. More flexible and maintainable code
4. Separation of concerns

Simple examples:

# Without DI - tight coupling
class UserService:
    def __init__(self):
        self.db = Database()  # Hardcoded dependency
        
    def get_user(self, id):
        return self.db.query(f"SELECT * FROM users WHERE id={id}")

# With DI - loose coupling
class UserService:
    def __init__(self, db):  # Dependency injected
        self.db = db
        
    def get_user(self, id):
        return self.db.query(f"SELECT * FROM users WHERE id={id}")
        
# Now we can easily inject different implementations:
prod_db = Database() 
test_db = MockDatabase()

prod_service = UserService(prod_db)  # For production
test_service = UserService(test_db)  # For testing
"""

"""
FastAPI Dependency Injection System Explanation

Key Concepts:
1. Dependencies are declared using the Depends() class
2. Can be used in path operation functions or other dependencies
3. Supports sync and async functions
4. Automatically handles dependency resolution order
   Example:
   async def get_db():
       return {"connected": True}
   
   async def get_user(db = Depends(get_db)):
       return {"user": "test", "db": db}
   
   async def get_items(user = Depends(get_user)):
       return {"items": [], "user": user}
   
   # FastAPI will resolve in correct order:
   # 1. First calls get_db()
   # 2. Then calls get_user() with db result
   # 3. Finally calls get_items() with user result
5. Provides built-in caching of dependencies within a request

Advantages over Flask:
1. Type hints and automatic validation
2. Built-in dependency resolution
3. More structured and explicit dependency management
4. Better support for testing via dependency overrides
5. Automatic OpenAPI documentation of dependencies

Example implementations below demonstrate:
1. Basic dependency injection
2. Dependencies with sub-dependencies
3. Class-based dependencies
4. Dependency caching
5. Dependency overrides for testing
"""

app = FastAPI()

# 1. Basic dependency
async def get_db():
    # Simulated DB connection
    db = {"connected": True}
    try:
        yield db
    finally:
        # Cleanup when request is done
        db["connected"] = False

# 2. Dependency with sub-dependency
async def get_current_user(db = Depends(get_db)):
    if not db["connected"]:
        raise HTTPException(status_code=500, detail="DB not connected")
    return {"username": "test_user"}

# 3. Class-based dependency
@dataclass
class CommonQueryParams:
    skip: int = 0
    limit: int = 100
    
    def __call__(self):
        return self

# 4. Cached dependency
def get_logger():
    return logging.getLogger(__name__)

@app.get("/users/")
async def read_users(
    commons: CommonQueryParams = Depends(CommonQueryParams),
    current_user: dict = Depends(get_current_user),
    logger: logging.Logger = Depends(get_logger)
):
    logger.info(f"Request from user: {current_user['username']}")
    return {
        "skip": commons.skip,
        "limit": commons.limit,
        "current_user": current_user
    }

# 5. Example of dependency override for testing
def override_get_current_user():
    return {"username": "test_override"}

# In tests:
# app.dependency_overrides[get_current_user] = override_get_current_user
"""
Composition vs Dependency Injection:

1. Composition
   - Object contains other objects as its parts
   - Tight coupling - dependencies are created inside the class
   - Less flexible for testing and changes
   Example:
   ```python
   class EmailService:
       def send_email(self, msg):
           pass
   
   class UserService:
       def __init__(self):
           # Tight coupling - EmailService created inside
           self._email = EmailService()
       
       def register(self, user):
           # Uses internal email service
           self._email.send_email("Welcome!")
   ```

2. Dependency Injection
   - Dependencies are passed in from outside
   - Loose coupling - class just declares what it needs
   - More flexible for testing and changing implementations
   Example:
   ```python
   class UserService:
       def __init__(self, email_service):
           # Loose coupling - email service injected
           self._email = email_service
       
       def register(self, user):
           self._email.send_email("Welcome!")
   
   # Can easily inject different implementations
   user_svc = UserService(email_service=MockEmailService())
   ```

Benefits of Dependency Injection:
- Easier testing with mocks
- Flexible to change implementations
- Clear dependencies
- Better separation of concerns
- More maintainable code

FastAPI uses DI via the Depends system to achieve these benefits.
"""

# Example demonstrating both approaches
class EmailNotifier:
    def notify(self, message: str):
        print(f"Sending email: {message}")

# Composition approach - tightly coupled
class UserManagerComposition:
    def __init__(self):
        # EmailNotifier created inside - hard to change/test
        self.notifier = EmailNotifier()
    
    def create_user(self, username: str):
        self.notifier.notify(f"Created user {username}")
        return {"username": username}

# Dependency Injection approach - loosely coupled
class UserManagerDI:
    def __init__(self, notifier):
        # Notifier injected from outside - flexible
        self.notifier = notifier
    
    def create_user(self, username: str):
        self.notifier.notify(f"Created user {username}")
        return {"username": username}

@app.post("/users/composition")
async def create_user_composition(username: str):
    manager = UserManagerComposition()
    return manager.create_user(username)

@app.post("/users/di")
async def create_user_di(
    username: str,
    notifier: EmailNotifier = Depends(EmailNotifier)
):
    manager = UserManagerDI(notifier)
    return manager.create_user(username)

    """
    Monkey Patching Example and Best Practices:
    
    Monkey patching is dynamically replacing methods/attributes at runtime.
    While powerful, it should be used with caution:
    
    PROS:
    - Useful for testing/mocking
    - Can hotfix third-party code
    - Enables runtime customization
    
    CONS:
    - Makes code harder to understand
    - Can lead to subtle bugs
    - Breaks code introspection
    - Makes debugging difficult
    - Can cause conflicts with other patches
    
    WHEN TO USE:
    1. Unit testing (with proper cleanup)
    2. Last resort fixes for third-party code
    3. Feature flags in development
    
    AVOID IN:
    1. Production code
    2. Public libraries
    3. Security-critical code
    """

    # Original class
    class PaymentProcessor:
        def process_payment(self, amount: float):
            # Imagine this makes a real API call
            print(f"Processing real payment of ${amount}")
            return {"status": "success", "amount": amount}

    # Example test using monkey patching - WITH PROPER SAFEGUARDS
    def test_payment_processing():
        # Store original method
        original_process = PaymentProcessor.process_payment
        
        # Replace with test double
        def mock_process(self, amount: float):
            print(f"Processing fake payment of ${amount}")
            return {"status": "success", "amount": amount}
            
        try:
            # Monkey patch the method
            PaymentProcessor.process_payment = mock_process
            
            # Use the patched class
            processor = PaymentProcessor()
            result = processor.process_payment(100.00)
            assert result["status"] == "success"
            
        finally:
            # IMPORTANT: Always restore original state
            PaymentProcessor.process_payment = original_process
            
    # Better alternative using dependency injection instead of monkey patching
    class TestablePaymentProcessor:
        def __init__(self, payment_service):
            self.payment_service = payment_service
            
        def process_payment(self, amount: float):
            return self.payment_service.process_payment(amount)

    # Example usage
    if __name__ == "__main__":
        test_payment_processing()
        print("Consider using dependency injection instead of monkey patching!")

