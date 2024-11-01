-- Create users table
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create trips table
CREATE TABLE trips (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create trip_locations table for tracking user movement
CREATE TABLE trip_locations (
    id BIGSERIAL PRIMARY KEY,
    trip_id BIGINT NOT NULL REFERENCES trips(id),
    coordinates POINT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    accuracy FLOAT,
    altitude FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_trips_user_id ON trips(user_id);
CREATE INDEX idx_trip_locations_trip_id ON trip_locations(trip_id);
CREATE INDEX idx_trip_locations_timestamp ON trip_locations(trip_id, timestamp);
CREATE INDEX idx_trip_locations_coordinates ON trip_locations USING GIST(coordinates);

-- Create photos table
CREATE TABLE photos (
    id BIGSERIAL PRIMARY KEY,
    trip_id BIGINT NOT NULL REFERENCES trips(id),
    filename VARCHAR(255) NOT NULL,
    coordinates POINT,
    taken_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_photos_trip_id ON photos(trip_id);
CREATE INDEX idx_photos_coordinates ON photos USING GIST(coordinates);


-- Insert sample users
INSERT INTO users (email, name) VALUES
    ('john.doe@example.com', 'John Doe'),
    ('jane.smith@example.com', 'Jane Smith'),
    ('mike.wilson@example.com', 'Mike Wilson');

-- Insert sample trips
INSERT INTO trips (user_id, title, description, start_date, end_date) VALUES
    (1, 'Europe Adventure', 'Backpacking across Western Europe', '2023-06-01', '2023-07-15'),
    (1, 'Asian Tour', 'Exploring Southeast Asia', '2023-09-01', '2023-10-15'),
    (2, 'African Safari', 'Wildlife photography tour', '2023-07-10', '2023-07-25'),
    (3, 'South America Trek', 'Hiking in the Andes', '2023-08-01', '2023-08-20');

-- Insert sample trip locations
INSERT INTO trip_locations (trip_id, coordinates, timestamp, accuracy, altitude) VALUES
    (1, POINT(2.3522, 48.8566), '2023-06-02 10:00:00', 10.5, 35.0),  -- Paris
    (1, POINT(12.4964, 41.9028), '2023-06-05 14:30:00', 8.2, 21.0),   -- Rome
    (2, POINT(100.5018, 13.7563), '2023-09-02 09:15:00', 12.1, 4.0),  -- Bangkok
    (2, POINT(103.8198, 1.3521), '2023-09-05 16:45:00', 5.8, 3.0),    -- Singapore
    (3, POINT(36.8219, -1.2921), '2023-07-11 07:30:00', 15.3, 1661.0), -- Nairobi
    (4, POINT(-72.5450, -13.1631), '2023-08-03 11:20:00', 20.1, 3399.0); -- Machu Picchu

-- Insert sample photos
INSERT INTO photos (trip_id, filename, coordinates, taken_at) VALUES
    (1, 'eiffel_tower.jpg', POINT(2.3522, 48.8566), '2023-06-02 10:30:00'),
    (1, 'colosseum.jpg', POINT(12.4964, 41.9028), '2023-06-05 15:00:00'),
    (2, 'grand_palace.jpg', POINT(100.5018, 13.7563), '2023-09-02 10:00:00'),
    (3, 'lion_pride.jpg', POINT(36.8219, -1.2921), '2023-07-11 08:15:00'),
    (4, 'machu_picchu.jpg', POINT(-72.5450, -13.1631), '2023-08-03 12:00:00');


-- SQL Interview Questions (Easy to Hard)

-- EASY
-- 1. Select all trips for user with id = 1





SELECT * FROM trips WHERE user_id = 1;

-- 2. Count number of photos per trip






SELECT trip_id, COUNT(*) as photo_count 
FROM photos 
GROUP BY trip_id;

-- MEDIUM 
-- 3. Get all trips with their location counts








SELECT t.id, t.title, COUNT(tl.id) as location_count
FROM trips t
LEFT JOIN trip_locations tl ON t.id = tl.trip_id
GROUP BY t.id, t.title;

-- 4. Find trips that have both photos and locations recorded








SELECT DISTINCT t.id, t.title
FROM trips t
INNER JOIN photos p ON t.id = p.trip_id
INNER JOIN trip_locations tl ON t.id = tl.trip_id;

-- HARD
-- 5. Find trips with locations within 100km of Paris (48.8566° N, 2.3522° E)








SELECT DISTINCT t.* 
FROM trips t
INNER JOIN trip_locations tl ON t.id = tl.trip_id
WHERE ST_DWithin(
    tl.coordinates::geography,
    ST_MakePoint(2.3522, 48.8566)::geography,
    100000
);

-- 6. Get users' travel statistics with window functions






SELECT 
    u.name,
    t.title,
    COUNT(tl.id) OVER (PARTITION BY t.id) as locations_in_trip,
    COUNT(tl.id) OVER (PARTITION BY u.id) as total_user_locations,
    FIRST_VALUE(tl.timestamp) OVER (
        PARTITION BY t.id 
        ORDER BY tl.timestamp
    ) as trip_first_location_time
FROM users u
JOIN trips t ON u.id = t.user_id
LEFT JOIN trip_locations tl ON t.id = tl.trip_id;

-- 7. Complex temporal query - Find overlapping trips for each user






WITH overlapping_trips AS (
    SELECT 
        t1.user_id,
        t1.id as trip1_id,
        t2.id as trip2_id,
        t1.title as trip1_title,
        t2.title as trip2_title
    FROM trips t1
    JOIN trips t2 ON 
        t1.user_id = t2.user_id AND
        t1.id < t2.id AND
        t1.start_date <= t2.end_date AND
        t2.start_date <= t1.end_date
)
SELECT * FROM overlapping_trips;
