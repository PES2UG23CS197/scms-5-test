DROP DATABASE IF EXISTS scms;
CREATE DATABASE scms;
USE scms;

-- Users Table
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    role ENUM('Admin', 'User') NOT NULL
) ENGINE=InnoDB;

-- Products Table
CREATE TABLE Products (
    sku VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    threshold INT DEFAULT 10
) ENGINE=InnoDB;

-- Inventory Table
CREATE TABLE Inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    sku VARCHAR(20) NOT NULL,
    location VARCHAR(100) NOT NULL,
    quantity INT DEFAULT 0 CHECK (quantity >= 0),
    FOREIGN KEY (sku) REFERENCES Products(sku),
    UNIQUE KEY unique_sku_location (sku, location)  
) ENGINE=InnoDB;

-- Orders Table
CREATE TABLE Orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    sku VARCHAR(20) NOT NULL,
    quantity INT NOT NULL,
    customer_name VARCHAR(100),
    customer_location VARCHAR(100) NOT NULL,
    status ENUM('Pending', 'Processed') DEFAULT 'Pending',
    FOREIGN KEY (sku) REFERENCES Products(sku),
    INDEX idx_status (status)  -- ✅ Faster filtering by order status
) ENGINE=InnoDB;

-- Logistics Table
CREATE TABLE Logistics (
    logistics_id INT AUTO_INCREMENT PRIMARY KEY,
    sku VARCHAR(20) NOT NULL,
    origin VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    transport_cost DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (sku) REFERENCES Products(sku)
) ENGINE=InnoDB;

-- Routes Table
CREATE TABLE Routes (
    route_id INT AUTO_INCREMENT PRIMARY KEY,
    origin VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    cost DECIMAL(10,2) NOT NULL,
    distance_km DECIMAL(6,2),
    UNIQUE KEY unique_route (origin, destination),  
    INDEX idx_origin_dest (origin, destination)     
) ENGINE=InnoDB;

-- Demand Forecast Table
CREATE TABLE DemandForecast (
    forecast_id INT AUTO_INCREMENT PRIMARY KEY,
    sku VARCHAR(20) NOT NULL,
    forecast_value INT NOT NULL,
    forecast_date DATE NOT NULL,
    FOREIGN KEY (sku) REFERENCES Products(sku)
) ENGINE=InnoDB;

-- Reports Table
CREATE TABLE Reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    generated_by VARCHAR(50) NOT NULL,
    summary TEXT
) ENGINE=InnoDB;

-- Logs Table
CREATE TABLE Logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    action TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
) ENGINE=InnoDB;

-- Sample Users
INSERT INTO Users (username, password, role) VALUES
('admin1', 'adminpass123', 'Admin'),
('user1', 'userpass123', 'User');

-- Sample Products
INSERT INTO Products (sku, name, description, threshold) VALUES
('SKU001', 'Laptop', 'High-performance laptop', 5),
('SKU002', 'Smartphone', 'Latest model smartphone', 10),
('SKU003', 'Router', 'Dual-band WiFi router', 8);

-- Sample Inventory
INSERT INTO Inventory (sku, location, quantity) VALUES
('SKU001', 'Warehouse A', 20),
('SKU002', 'Warehouse B', 15),
('SKU003', 'Warehouse A', 5);

-- Sample Logistics
-- INSERT INTO Logistics (sku, origin, destination, transport_cost) VALUES
-- ('SKU001', 'Warehouse A', 'Retail Hub 1', 150.00),
-- ('SKU002', 'Warehouse B', 'Retail Hub 2', 120.00),
-- ('SKU003', 'Warehouse A', 'Retail Hub 3', 90.00);

-- Sample Routes
INSERT INTO Routes (origin, destination, cost, distance_km) VALUES
('Warehouse A', 'Retail Hub 1', 150.00, 25.5),
('Warehouse A', 'Retail Hub 2', 120.00, 5.0),
('Warehouse A', 'Retail Hub 3', 90.00, 10.0),
('Warehouse B', 'Retail Hub 1', 70.00, 15.0),
('Warehouse B', 'Retail Hub 2', 100.00, 25.0),
('Warehouse B', 'Retail Hub 3', 175.00, 30.0),
('Warehouse B', 'Warehouse A', 80.00, 20.0),
('Warehouse A', 'Warehouse B', 100.00, 30.0);

-- Sample Orders
-- INSERT INTO Orders (sku, quantity, customer_name, customer_location, status) VALUES
-- ('SKU001', 2, 'Alice', 'Retail Hub 1', 'Pending'),
-- ('SKU002', 1, 'Bob', 'Retail Hub 2', 'Processed'),
-- ('SKU003', 3, 'Charlie', 'Retail Hub 3', 'Pending');

-- Sample Forecast
-- INSERT INTO DemandForecast (sku, forecast_value, forecast_date) VALUES
-- ('SKU001', 10, '2025-11-10'),
-- ('SKU002', 15, '2025-11-12'),
-- ('SKU003', 8, '2025-11-15');

-- Sample Queries 
SELECT * FROM Users; 
SELECT * FROM Products; 
SELECT * FROM Inventory; 
SELECT * FROM Orders; 
SELECT * FROM Logistics; 
SELECT * FROM Routes; 
SELECT * FROM DemandForecast; 
SELECT * FROM Reports; 
SELECT * FROM Logs;
