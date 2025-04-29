-- Set schema
SET search_path TO taxi_management;

-- Insert Managers
INSERT INTO MANAGER (NAME, SSN, EMAIL) VALUES 
('Alice Manager', '111223333', 'alice.manager@example.com'),
('Bob Supervisor', '222334444', 'bob.supervisor@example.com');

-- Insert Addresses
INSERT INTO ADDRESS (ROAD, NUMBER, CITY) VALUES 
('Main St', '100', 'Metropolis'),
('Second St', '200', 'Gotham'),
('Third Ave', '300', 'Star City'),
('Fourth Blvd', '400', 'Central City');

-- Insert Clients
INSERT INTO CLIENT (NAME, EMAIL) VALUES 
('Charlie Client', 'charlie@example.com'),
('Diana Client', 'diana@example.com'),
('Eddie Client', 'eddie@example.com');

-- Insert HasAddress
INSERT INTO HasAddress (EMAIL, ROAD, NUMBER, CITY) VALUES
('charlie@example.com', 'Main St', '100', 'Metropolis'),
('diana@example.com', 'Second St', '200', 'Gotham'),
('eddie@example.com', 'Third Ave', '300', 'Star City');

-- Insert Drivers
INSERT INTO DRIVER (NAME, ROAD, NUMBER, CITY) VALUES 
('Frank Driver', 'Fourth Blvd', '400', 'Central City'),
('Grace Driver', 'Main St', '100', 'Metropolis');

-- Insert Cars
INSERT INTO CAR (CAR_ID, BRAND) VALUES 
(1, 'Toyota'),
(2, 'Ford');

-- Insert Models
INSERT INTO MODEL (MODEL_ID, TRANSMISSION, YEAR, COLOR, CAR_ID) VALUES 
(101, 'Automatic', 2022, 'Red', 1),
(102, 'Manual', 2021, 'Blue', 1),
(201, 'Automatic', 2023, 'Black', 2);

-- Insert CanDrive
INSERT INTO CAN_DRIVE (NAME, MODEL_ID, CAR_ID) VALUES
('Frank Driver', 101, 1),
('Grace Driver', 102, 1),
('Grace Driver', 201, 2);

-- Insert Rents (including multiple rents per client)
INSERT INTO RENT (RENT_ID, RENT_DATE, EMAIL, NAME, MODEL_ID, CAR_ID) VALUES 
(1, '2024-01-10', 'charlie@example.com', 'Frank Driver', 101, 1),
(2, '2024-01-15', 'charlie@example.com', 'Grace Driver', 102, 1),
(3, '2024-02-01', 'diana@example.com', 'Grace Driver', 102, 1),
(4, '2024-02-20', 'eddie@example.com', 'Grace Driver', 201, 2),
(5, '2024-03-05', 'charlie@example.com', 'Frank Driver', 101, 1);

-- Insert Reviews (multiple reviews per driver)
INSERT INTO REVIEW (REVIEW_ID, RATING, MESSAGE, NAME, EMAIL) VALUES 
(1, 5, 'Great ride!', 'Frank Driver', 'charlie@example.com'),
(2, 4, 'Smooth and on time.', 'Grace Driver', 'diana@example.com'),
(3, 3, 'Okay service.', 'Grace Driver', 'eddie@example.com'),
(4, 5, 'Excellent driver!', 'Frank Driver', 'charlie@example.com');

-- Insert Credit Cards
INSERT INTO CREDIT_CARD (NUMBER, EMAIL, ROAD, NUMBER_ADDR, CITY) VALUES 
('1234567812345678', 'charlie@example.com', 'Main St', '100', 'Metropolis'),
('2345678923456789', 'diana@example.com', 'Second St', '200', 'Gotham'),
('3456789034567890', 'eddie@example.com', 'Third Ave', '300', 'Star City');
