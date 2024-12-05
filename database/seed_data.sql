USE voya_db;

INSERT INTO Flights (origin, destination, departure_time, arrival_time, cost, airline, flight_number)
VALUES
('San Francisco', 'New York', '2024-12-10 18:00:00', '2024-12-11 02:00:00', 350.00, 'Delta Airlines', 'DL123'),
('San Francisco', 'New York', '2024-12-15 08:00:00', '2024-12-15 16:00:00', 400.00, 'American Airlines', 'AA456'),
('San Francisco', 'New York', '2024-12-12 12:30:00', '2024-12-12 20:00:00', 275.00, 'United Airlines', 'UA789'),
('San Francisco', 'New York', '2024-12-18 07:00:00', '2024-12-18 15:30:00', 180.00, 'Alaska Airlines', 'AS101'),
('San Francisco', 'New York', '2024-12-20 16:00:00', '2024-12-20 23:30:00', 320.00, 'Southwest Airlines', 'SW202');

INSERT INTO Hotels (name, address, cost_per_night)
VALUES
('Marriott Marquis', '1535 Broadway, New York, NY 10036', 450.00),
('Hilton Times Square', '234 W 42nd St, New York, NY 10036', 320.00),
('The Plaza Hotel', '768 5th Ave, New York, NY 10019', 550.00),
('Hotel Edison', '228 W 47th St, New York, NY 10036', 290.00),
('InterContinental New York Barclay', '111 E 48th St, New York, NY 10017', 400.00);

INSERT INTO Restaurants (name, address, cost_per_person, cuisine)
VALUES
('Gramercy Tavern', '42 E 20th St, New York, NY 10003', 75.00, 'American'),
('Le Bernardin', '155 W 51st St, New York, NY 10019', 90.00, 'Seafood'),
('Joe’s Shanghai', '46 Bowery St, New York, NY 10013', 40.00, 'Chinese'),
('Lombardi’s Pizza', '32 Spring St, New York, NY 10012', 25.00, 'Italian'),
('Katz’s Delicatessen', '205 E Houston St, New York, NY 10002', 30.00, 'Deli');

INSERT INTO Rides (origin, destination, estimated_cost, provider)
VALUES
('John F. Kennedy International Airport', 'Marriott Marquis, 1535 Broadway, New York, NY 10036', 60.00, 'Uber'),
('LaGuardia Airport', 'Hilton Times Square, 234 W 42nd St, New York, NY 10036', 45.00, 'Lyft'),
('Newark Liberty International Airport', 'The Plaza Hotel, 768 5th Ave, New York, NY 10019', 70.00, 'Uber'),
('Penn Station', 'Hotel Edison, 228 W 47th St, New York, NY 10036', 25.00, 'Lyft'),
('Grand Central Terminal', 'InterContinental New York Barclay, 111 E 48th St, New York, NY 10017', 30.00, 'Uber');