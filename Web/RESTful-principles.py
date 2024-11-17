# list of principles for RESTful API design
# 1. Uniform Interface. in simpler words, using HTTP methods to interact with resources.
# GOOD: GET /users/123
# BAD: GET users/123/details => why? because the resource is not uniform. 
# 2. Client-Server. the client and server are separate entities, and the client makes requests to the server and the server responds to the client.
# 3. Stateless. each request from the client to the server must contain all the information necessary to understand the request and process it.
# GOOD: GET /users/123
# BAD: GET /users/123?session_id=456
# 4. Cacheable
# 5. Layered System
# 6. Code on Demand (optional)
# 7. Idempotency


# HTTP methods
# GET: retrieve a resource
# POST: create a resource
# PUT: update a resource
# DELETE: delete a resource
# PATCH: update a resource partially
# OPTIONS: get the supported HTTP methods
# HEAD: get the metadata of a resource without the body
# CONNECT: establish a tunnel to the server identified by the target resource
# TRACE: perform a message loop-back test along the path to the target resource
