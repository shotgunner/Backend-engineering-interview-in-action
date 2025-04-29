# Message Queues and Event-Driven Architecture

## Table of Contents
1. [Message Queue Fundamentals](#message-queue-fundamentals)
2. [Kafka vs RabbitMQ](#kafka-vs-rabbitmq)
3. [Event Sourcing Patterns](#event-sourcing-patterns)
4. [Message Delivery Guarantees](#message-delivery-guarantees)
5. [Dead Letter Queues](#dead-letter-queues)
6. [Partitioning Strategies](#partitioning-strategies)
7. [Interview Questions](#interview-questions)
8. [Common Pitfalls](#common-pitfalls)

## Message Queue Fundamentals

### Key Concepts
- **Message**: Immutable packet of data
- **Queue**: FIFO data structure for messages
- **Topic**: Named destination for messages
- **Producer**: Application that sends messages
- **Consumer**: Application that receives messages
- **Broker**: Server that hosts queues/topics

### Use Cases
1. Asynchronous Processing
2. Workload Distribution
3. Event Broadcasting
4. System Decoupling
5. Peak Load Handling

## Kafka vs RabbitMQ

### Apache Kafka
```plaintext
Strengths:
- High throughput (1M+ msgs/sec)
- Persistent storage by default
- Natural partitioning
- Great for event sourcing
- Stream processing

Use Cases:
- Log aggregation
- Stream processing
- Event sourcing
- Metrics collection
```

### RabbitMQ
```plaintext
Strengths:
- Multiple messaging protocols
- Complex routing
- Lower latency
- Traditional queue semantics
- Lower resource usage

Use Cases:
- Traditional queuing
- RPC patterns
- Complex routing needs
- When message order matters
```

### Comparison Table
| Feature | Kafka | RabbitMQ |
|---------|-------|----------|
| Performance | 100k-1M+ msgs/sec | 20k-50k msgs/sec |
| Message Persistence | Default | Optional |
| Message Routing | Simple | Complex/Flexible |
| Ordering | Per partition | Per queue |
| Replication | Built-in | Plugin |
| Protocol | Custom TCP | AMQP, MQTT, STOMP |

## Event Sourcing Patterns

### Basic Pattern
```python
class BankAccount:
    def __init__(self):
        self.balance = 0
        self.events = []

    def apply_event(self, event):
        if event.type == "DEPOSIT":
            self.balance += event.amount
        elif event.type == "WITHDRAWAL":
            self.balance -= event.amount
        self.events.append(event)

    def get_balance(self):
        return self.balance

    def deposit(self, amount):
        event = Event("DEPOSIT", amount)
        self.apply_event(event)
        return event

    def withdraw(self, amount):
        if amount <= self.balance:
            event = Event("WITHDRAWAL", amount)
            self.apply_event(event)
            return event
        raise InsufficientFunds()
```

### Event Store
```sql
CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    aggregate_id UUID NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_events_aggregate ON events(aggregate_id);
```

## Message Delivery Guarantees

### At Most Once
```python
def process_message(message):
    try:
        process(message)
        ack(message)
    except:
        # Message is lost if processing fails
        pass
```

### At Least Once
```python
def process_message(message):
    try:
        process(message)
    finally:
        ack(message)  # Always ack, might process twice
```

### Exactly Once
```python
def process_message(message):
    if is_duplicate(message.id):
        ack(message)
        return
    
    try:
        with transaction():
            process(message)
            store_processed_id(message.id)
            ack(message)
    except:
        # Message will be retried
        pass
```

## Dead Letter Queues

### Implementation Example
```python
class MessageProcessor:
    def __init__(self, max_retries=3):
        self.max_retries = max_retries
        self.main_queue = Queue("main")
        self.dlq = Queue("deadletter")
    
    def process_message(self, message):
        try:
            if message.retries >= self.max_retries:
                self.move_to_dlq(message)
                return
            
            self.process(message)
            self.ack(message)
            
        except TemporaryError:
            message.retries += 1
            self.main_queue.requeue(message)
            
        except PermanentError:
            self.move_to_dlq(message)
    
    def move_to_dlq(self, message):
        self.dlq.send(message)
        self.ack(message)
```

## Partitioning Strategies

### Key-Based Partitioning
```python
def get_partition(key, total_partitions):
    return hash(key) % total_partitions

# Example usage
class OrderProducer:
    def send_order(self, order):
        partition = get_partition(order.customer_id, 
                                total_partitions=10)
        kafka.send(topic="orders",
                  key=order.customer_id,
                  value=order,
                  partition=partition)
```

### Round-Robin
```python
class LoadBalancedProducer:
    def __init__(self):
        self.current_partition = 0
        self.total_partitions = 10
    
    def get_next_partition(self):
        partition = self.current_partition
        self.current_partition = (self.current_partition + 1) % self.total_partitions
        return partition
```

## Interview Questions

1. **Q**: How would you ensure message ordering in a distributed system?
   **A**: Options include:
   - Single partition for related messages
   - Sequence numbers + reordering buffer
   - Event sourcing with version numbers

2. **Q**: How do you handle poison messages?
   **A**: Implement:
   - Retry limits
   - Dead letter queues
   - Error logging and monitoring
   - Message inspection tools

3. **Q**: Compare Kafka and RabbitMQ for high-throughput scenarios
   **A**: Consider:
   - Kafka for highest throughput
   - RabbitMQ for complex routing
   - Resource usage vs scalability
   - Operational complexity

## Common Pitfalls

1. **Message Persistence**
   - Not configuring proper persistence
   - Losing messages during broker restart
   - No backup/recovery strategy

2. **Consumer Groups**
   - Incorrect partition assignment
   - Rebalancing issues
   - Consumer lag monitoring

3. **Resource Management**
   - Memory leaks in consumers
   - Connection pool exhaustion
   - Disk space for persistent queues

4. **Error Handling**
   - Infinite retry loops
   - Missing dead letter queues
   - Silent failures

### Further Reading
- [Designing Data-Intensive Applications](https://dataintensive.net/)
- [Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/)
- [Kafka Documentation](https://kafka.apache.org/documentation/)
- [RabbitMQ Documentation](https://www.rabbitmq.com/documentation.html)