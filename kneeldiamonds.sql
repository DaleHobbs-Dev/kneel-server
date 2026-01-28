-- Run this block if you already have a database and need to re-create it
DELETE FROM Metals;
DELETE FROM Styles;
DELETE FROM Sizes;
DELETE FROM Customers;
DELETE FROM Orders;

DROP TABLE IF EXISTS Metals;
DROP TABLE IF EXISTS Styles;
DROP TABLE IF EXISTS Sizes;
DROP TABLE IF EXISTS Customers;
DROP TABLE IF EXISTS Orders;
-- End block

CREATE TABLE `Metals`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `metal` NVARCHAR(160) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);

CREATE TABLE `Styles`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `name` NVARCHAR(160) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);

CREATE TABLE `Sizes`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `carets` NUMERIC(3,2) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);

CREATE TABLE `Customers`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `name` NVARCHAR(160) NOT NULL,
    `email` NVARCHAR(255) NOT NULL,
    `address` NVARCHAR(255) NOT NULL
);

CREATE TABLE `Orders`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `metalId` INTEGER NOT NULL,
    `styleId` INTEGER NOT NULL,
    `sizeId` INTEGER NOT NULL,
    `customerId` INTEGER NOT NULL,
    `timestamp` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`metalId`) REFERENCES `Metals`(`id`),
    FOREIGN KEY (`styleId`) REFERENCES `Styles`(`id`),
    FOREIGN KEY (`sizeId`) REFERENCES `Sizes`(`id`),
    FOREIGN KEY (`customerId`) REFERENCES `Customers`(`id`)
);

-- Insert styles
INSERT INTO styles (id, name, price) VALUES (1, 'Classic', 500);
INSERT INTO styles (id, name, price) VALUES (2, 'Modern', 710);
INSERT INTO styles (id, name, price) VALUES (3, 'Vintage', 965);

-- Insert sizes
INSERT INTO sizes (id, carets, price) VALUES (1, 0.5, 405);
INSERT INTO sizes (id, carets, price) VALUES (2, 0.75, 782);
INSERT INTO sizes (id, carets, price) VALUES (3, 1, 1470);
INSERT INTO sizes (id, carets, price) VALUES (4, 1.5, 1997);
INSERT INTO sizes (id, carets, price) VALUES (5, 2, 3638);
-- Insert metals
INSERT INTO metals (id, metal, price) VALUES (1, 'Sterling Silver', 12.42);
INSERT INTO metals (id, metal, price) VALUES (2, '14K Gold', 736.4);
INSERT INTO metals (id, metal, price) VALUES (3, '24K Gold', 1258.9);
INSERT INTO metals (id, metal, price) VALUES (4, 'Platinum', 795.45);
INSERT INTO metals (id, metal, price) VALUES (5, 'Palladium', 1241);

-- Insert customer
INSERT INTO Customers (id, name, email, address) VALUES (1, 'John Smith', 'john.smith@example.com', '123 Main St, Nashville, TN 37201');
INSERT INTO Customers (id, name, email, address) VALUES (2, 'Jane Doe', 'jane.doe@example.com', '456 Elm St, Nashville, TN 37202');
INSERT INTO Customers (id, name, email, address) VALUES (3, 'Alice Johnson', 'alice.johnson@example.com', '789 Oak St, Nashville, TN 37203');

-- Insert orders
INSERT INTO orders (id, metalId, styleId, sizeId, customerId) VALUES (1, 2, 1, 4, 1);
INSERT INTO orders (id, metalId, styleId, sizeId, customerId) VALUES (2, 3, 2, 3, 2);
INSERT INTO orders (id, metalId, styleId, sizeId, customerId) VALUES (3, 1, 3, 1, 3);

SELECT * FROM metals;
SELECT * FROM styles;