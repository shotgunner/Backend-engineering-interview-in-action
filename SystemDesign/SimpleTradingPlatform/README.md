# Simple Trading Platform Example

This system is a simplified example of a trading platform where users can submit buy orders for stocks. It demonstrates the use of a message queue (Kafka) for processing trades asynchronously and a database (SQLite) for storing trade information.

## Components

*   **Web Application (`app.py`)**:
    *   A Flask-based web server that exposes an API endpoint for placing buy orders.
    *   It validates incoming requests, records trades in the database, and publishes trade events to a Kafka topic.
*   **Database (`trading.db`)**:
    *   An SQLite database to store trade records.
    *   The schema includes `trades` table with columns like `user_id`, `symbol`, `quantity`, `price`, and `timestamp`.
*   **Message Queue (Kafka)**:
    *   Used to decouple the trade submission process from further processing (e.g., matching engines, notifications, analytics).
    *   The application acts as a Kafka producer, sending trade events to a `trades` topic.

## Setup and Running

1.  **Prerequisites**:
    *   Python 3.x
    *   Flask (`pip install Flask`)
    *   Kafka client for Python (`pip install kafka-python`)
    *   A running Kafka instance (e.g., local Docker setup or cloud service). Ensure the `trades` topic is created.
    *   SQLite (usually comes with Python).

2.  **Configure Kafka**:
    *   Update the `bootstrap_servers` in `app.py` if your Kafka instance is not running on `localhost:9092`.

3.  **Initialize Database**:
    *   When you first run `app.py`, it will automatically create the `trading.db` file and the `trades` table if they don't exist.

4.  **Run the Application**:
    ```bash
    python app.py
    ```
    The Flask development server will start (usually on `http://127.0.0.1:5000`).

5.  **Placing a Buy Order**:
    *   Send a POST request to the `/buy` endpoint with a JSON payload:
        ```json
        {
            "symbol": "AAPL",
            "quantity": 10,
            "price": 150.00
        }
        ```
    *   Include a `User-Id` header with a unique user identifier:
        ```
        User-Id: user123
        ```
    *   Example using `curl`:
        ```bash
        curl -X POST -H "Content-Type: application/json" -H "User-Id: user123" -d '{"symbol": "AAPL", "quantity": 10, "price": 150.00}' http://127.0.0.1:5000/buy
        ```

## Potential Interview Questions

*   **Scalability**:
    *   How would you scale this system to handle millions of users and trades per second? (e.g., multiple app instances, load balancers, database scaling, Kafka partitions).
    *   What are the bottlenecks in the current design?
*   **Reliability**:
    *   How can you ensure that trades are not lost if the application crashes? (e.g., Kafka persistence, consumer acknowledgments, idempotent processing).
    *   What happens if Kafka is down?
*   **Choice of Technology**:
    *   Why use Kafka here? What are alternatives? (e.g., RabbitMQ, Redis Streams).
    *   Pros and cons of using SQLite? When would you choose a different database? (e.g., PostgreSQL, MySQL, NoSQL).
*   **API Design**:
    *   How could the API be improved? (e.g., authentication, different order types like sell orders, market vs. limit orders).
*   **Data Model**:
    *   How would you extend the data model to include user accounts, stock information, or order status?
*   **Further Processing**:
    *   What other services might consume the trade events from Kafka? (e.g., order matching engine, risk management, notifications service, analytics pipeline).
