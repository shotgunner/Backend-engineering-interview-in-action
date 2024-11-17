# why do we need depend in fast-api?

# Dependencies are used to inject external resources or services into the application.
# They are typically used for things like databases, external APIs, or other shared resources.
# This separation of concerns helps in managing complexity and making the code more modular and easier to maintain.

from fastapi import FastAPI, HTTPException
from typing import Optional


app = FastAPI()

# Bad Example - Without Dependency Injection
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    # Database connection logic mixed with route handler
    try:
        # Imagine this connects to a database
        db = Database()  # Creating connection in route
        user = db.get_user(user_id)
        db.close()  # Need to remember to close
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Good Example - With Dependency Injection
from fastapi import Depends

class DatabaseService:
    def __init__(self):
        # Initialize database connection
        self.db = None
    
    def get_user(self, user_id: int):
        # Simulated database query
        return {"id": user_id, "name": "John Doe"}

# Create dependency
def get_db():
    db = DatabaseService()
    try:
        yield db
    finally:
        if db.db:
            db.db.close()

@app.get("/users_better/{user_id}")
async def get_user_better(
    user_id: int,
    db: DatabaseService = Depends(get_db)
):
    try:
        return db.get_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Benefits of using Depends:
# 1. Separation of concerns
# 2. Easier testing (can mock dependencies)
# 3. Automatic cleanup of resources
# 4. Code reusability
# 5. Better error handling

