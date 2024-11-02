# System Design Interview: Polarsteps Travel App

## 1. Problem Understanding & Requirements

### Functional Requirements
- Users can track their trips and routes in real-time
- Support photo/video uploads with location tagging
- Generate travel stories/blogs automatically
- Share trips with friends/family
- Offline functionality for tracking without internet
- Support trip statistics (distance, countries, etc.)

### Non-Functional Requirements
- High availability (99.9%)
- Low latency for real-time tracking
- Data consistency for trip information
- Scalability to handle millions of users
- Security for user data and privacy
- Efficient storage for media files

## 2. Scale Estimation

### Traffic Estimates
- DAU (Daily Active Users): 1M
- Average API requests per user per day: 50
- Total daily requests: 50M
- QPS (Queries Per Second): ~580 (50M/86400)
- Peak QPS: 1160 (2x average)

### Storage Estimates
- Trip data per user per year: ~1MB
- Photo/video storage per user per year: ~500MB
- Total annual storage for 1M users: 501TB
- 5-year projection: 2.5PB

## 3. System API Design


