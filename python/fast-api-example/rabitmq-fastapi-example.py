from fastapi import FastAPI, HTTPException
from aio_pika import connect_robust, Message
import json

app = FastAPI()

# RabbitMQ connection configuration
RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"

async def get_rabbitmq_connection():
    try:
        # Create a robust connection to RabbitMQ
        connection = await connect_robust(RABBITMQ_URL)
        return connection
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to RabbitMQ: {str(e)}")

@app.post("/publish/{queue_name}")
async def publish_message(queue_name: str, message: dict):
    # Get RabbitMQ connection
    connection = await get_rabbitmq_connection()
    
    try:
        # Create a channel
        channel = await connection.channel()
        
        # Declare a queue
        queue = await channel.declare_queue(queue_name, durable=True)
        
        # Convert message to JSON and encode
        message_body = json.dumps(message).encode()
        
        # Create and publish the message
        await channel.default_exchange.publish(
            Message(message_body),
            routing_key=queue_name
        )
        
        return {"status": "success", "message": "Message published successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to publish message: {str(e)}")
    
    finally:
        await connection.close()

@app.get("/consume/{queue_name}")
async def consume_message(queue_name: str):
    connection = await get_rabbitmq_connection()
    
    try:
        # Create a channel
        channel = await connection.channel()
        
        # Declare a queue
        queue = await channel.declare_queue(queue_name, durable=True)
        
        # Get one message from the queue
        message = await queue.get(timeout=5)
        
        if message is None:
            return {"status": "empty", "message": "No messages in queue"}
            
        # Acknowledge the message
        await message.ack()
        
        # Decode and parse the message
        body = json.loads(message.body.decode())
        
        return {"status": "success", "message": body}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to consume message: {str(e)}")
    
    finally:
        await connection.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
