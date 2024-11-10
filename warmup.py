from fastapi import FastAPI

from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import sqlite3
from fastapi import HTTPException, Depends, status

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Models
class User(BaseModel):
    id: Optional[int] = None
    email: str
    name: str
    created_at: Optional[datetime] = None

class Trip(BaseModel):
    id: Optional[int] = None
    user_id: int
    title: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime

class Photo(BaseModel):
    id: Optional[int] = None
    trip_id: int
    filename: str
    coordinates: Optional[tuple] = None
    taken_at: Optional[datetime] = None

# Database connection
def get_db():
    conn = sqlite3.connect('travel.db')
    try:
        conn.row_factory = sqlite3.Row
        yield conn
    finally:
        conn.close()

# Authentication middleware (simplified)
async def get_current_user(db: sqlite3.Connection = Depends(get_db)):
    # In real app, would verify JWT token
    return {"id": 1, "email": "test@example.com"}

# CRUD Operations
@app.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO users (email, name) VALUES (?, ?) RETURNING *",
        (user.email, user.name)
    )
    db.commit()
    return dict(cursor.fetchone())

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    result = cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = result.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(user)

# Trips endpoints
@app.post("/trips/", response_model=Trip)
async def create_trip(
    trip: Trip,
    current_user = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute(
        """INSERT INTO trips (user_id, title, description, start_date, end_date)
        VALUES (?, ?, ?, ?, ?) RETURNING *""",
        (current_user["id"], trip.title, trip.description, 
            trip.start_date, trip.end_date)
    )
    db.commit()
    return dict(cursor.fetchone())

@app.get("/trips/", response_model=List[Trip])
async def list_trips(
    skip: int = 0,
    limit: int = 10,
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM trips LIMIT ? OFFSET ?",
        (limit, skip)
    )
    return [dict(row) for row in cursor.fetchall()]

# Search endpoint with filtering
@app.get("/search/trips/")
async def search_trips(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    title: Optional[str] = None,
    db: sqlite3.Connection = Depends(get_db)
):
    query = "SELECT * FROM trips WHERE 1=1"
    params = []
    
    if start_date:
        query += " AND start_date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND end_date <= ?"
        params.append(end_date)
    if title:
        query += " AND title LIKE ?"
        params.append(f"%{title}%")
        
    cursor = db.cursor()
    cursor.execute(query, params)
    return [dict(row) for row in cursor.fetchall()]

# File upload endpoint
@app.post("/trips/{trip_id}/photos/")
async def upload_photo(
    trip_id: int,
    photo: Photo,
    current_user = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db)
):
    # Verify trip belongs to user
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM trips WHERE id = ? AND user_id = ?",
        (trip_id, current_user["id"])
    )
    if not cursor.fetchone():
        raise HTTPException(
            status_code=403,
            detail="Not authorized to upload to this trip"
        )
        
    cursor.execute(
        """INSERT INTO photos (trip_id, filename, coordinates, taken_at)
        VALUES (?, ?, ?, ?) RETURNING *""",
        (trip_id, photo.filename, photo.coordinates, photo.taken_at)
    )
    db.commit()
    return dict(cursor.fetchone())

# Aggregation endpoint
@app.get("/trips/stats/")
async def get_trip_stats(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("""
        SELECT 
            COUNT(*) as total_trips,
            AVG(JULIANDAY(end_date) - JULIANDAY(start_date)) as avg_duration,
            COUNT(DISTINCT user_id) as unique_users
        FROM trips
    """)
    return dict(cursor.fetchone())

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "1.0.0"
    }
