# Trip Sharing Application Example

This system is an example of an application that allows users to create, manage, and share travel routes. It demonstrates API design with Flask, data modeling with SQLAlchemy, and features like pagination and sharing.

The main application logic is in `design-system-app.py`.

## Components

*   **Web Application (`design-system-app.py`)**:
    *   A Flask-based web server that exposes RESTful APIs for managing travel routes.
    *   Uses Flask-SQLAlchemy for ORM and database interaction.
*   **Database (`travel_routes.db`)**:
    *   An SQLite database to store user information, routes, and sharing details.
    *   **Models**:
        *   `User`: Stores user information.
        *   `Route`: Stores details about travel routes, linked to a user.
        *   `RouteShare`: Manages which routes are shared with which users.

## Setup and Running

1.  **Prerequisites**:
    *   Python 3.x
    *   Flask (`pip install Flask`)
    *   Flask-SQLAlchemy (`pip install Flask-SQLAlchemy`)
    *   SQLite (usually comes with Python).

2.  **Initialize Database**:
    *   When you first run `design-system-app.py`, it will automatically create the `travel_routes.db` file and the necessary tables if they don't exist (due to `db.create_all()`).

3.  **Run the Application**:
    ```bash
    python design-system-app.py
    ```
    The Flask development server will start (usually on `http://127.0.0.1:5000`).

## API Endpoints

*   **`GET /api/routes`**:
    *   Fetches a paginated list of routes.
    *   Query Parameters: `page`, `per_page`, `user_id` (optional, to filter by user).
*   **`POST /api/routes/<int:route_id>/share`**:
    *   Shares a specific route with another user.
    *   Request Body (JSON): `{"user_id": <shared_with_user_id>}`
*   **`GET /api/routes/shared-with-me`**:
    *   Fetches routes shared with the specified user.
    *   Query Parameters: `page`, `per_page`, `user_id` (mandatory).

*(Note: User creation and authentication are not implemented in this example but would be essential for a production system.)*

## Potential Interview Questions

*   **API Design**:
    *   How would you implement user registration and authentication? (e.g., JWT, OAuth).
    *   What other API endpoints might be useful? (e.g., creating routes, updating routes, deleting routes, searching routes).
    *   How would you handle API versioning?
*   **Database Design**:
    *   Discuss the choice of database (SQLite). What are the pros and cons for this application? When might you choose PostgreSQL or a NoSQL database?
    *   How would you model more complex route information (e.g., waypoints, locations, maps integration)?
    *   How can you optimize database queries, especially for shared routes or popular routes?
*   **Scalability & Performance**:
    *   How would you scale the application to handle many users and routes?
    *   Discuss caching strategies for frequently accessed routes or user data.
*   **Features**:
    *   How would you implement real-time collaboration on routes? (e.g., WebSockets).
    *   How would you add a notification system for when routes are shared?
*   **`usecase1.md`**:
    *   The file `usecase1.md` in this directory outlines a specific scenario. Discuss how the current API and data model support this use case and what enhancements might be needed.
