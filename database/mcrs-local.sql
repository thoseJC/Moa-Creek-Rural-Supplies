DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS user_roles;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS payment;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS address;
DROP TABLE IF EXISTS invoice;


CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    parent_id INT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    ct_image_path VARCHAR(255),
    FOREIGN KEY (parent_id) REFERENCES categories(category_id) ON DELETE SET NULL
);


CREATE TABLE products (
    product_id int auto_increment PRIMARY KEY,
    category_id INT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    pd_image_path VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    quantity INT DEFAULT 0,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);


CREATE TABLE user_roles (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE users (
    user_id VARCHAR(36) PRIMARY KEY,
    role_id INT,
    first_name VARCHAR(250) NOT NULL,
    last_name VARCHAR(250) NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR (20),
    loyalty_points int DEFAULT 0,
    user_password VARCHAR(255) NOT NULL,
    shipping_address TEXT,
    status BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (role_id) REFERENCES user_roles(role_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE payment (
    payment_id VARCHAR(36) primary KEY,
    user_id VARCHAR(36) NOT NULL ,
    total decimal(10,2) NOT NULL,
    payment_type VARCHAR(20),
    GST decimal(10,2) NOT NULL,
    paid_date timestamp DEFAULT  CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY key,
    user_id VARCHAR(36) not null,
    payment_id VARCHAR(36), -- use to define whether an order has been paid or not
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10, 2) NOT NULL,
    GST decimal(10,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending', -- Example statuses: pending, completed, cancelled
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (payment_id) REFERENCES payment (payment_id)
);

CREATE TABLE order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    price_per_unit DECIMAL(10, 2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE invoice(
    invoice_id VARCHAR(36) primary KEY,
    user_id varchar(36) not NULL,
    GST DECIMAL(10,2) not NULL,
    total DECIMAL(10,2) NOT NULL,
    invoice_date timestamp DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


INSERT INTO user_roles (role_name) VALUES ('manager'), ('customer'), ('admin'), ('staff');

INSERT INTO users (user_id, role_id, first_name, last_name, username, email, password, status) 
VALUES 
    (UUID(), (SELECT role_id FROM user_roles WHERE role_name = 'manager'), 'Monica', 'Briggs', 'manager', 'manager@manager.com', '123456', TRUE),
    (UUID(), (SELECT role_id FROM user_roles WHERE role_name = 'customer'), 'Forrest', 'Curtis', 'customer', 'customer@customer.com', '123456', TRUE),
    (UUID(), (SELECT role_id FROM user_roles WHERE role_name = 'admin'), 'Basil', 'Parker', 'admin', 'admin@admin.com', '123456', TRUE),
    (UUID(), (SELECT role_id FROM user_roles WHERE role_name = 'staff'), 'Harley', 'Stephenson', 'staff', 'staff@staff.com', '123456', TRUE);


INSERT INTO categories (name, parent_id, description, ct_image_path) VALUES
('Animal Health Care', NULL, 'Products aimed at maintaining animal health.', 'images/category_image/animal_healthcare.jpg'),
('Animal Feed & Nutrition', NULL, 'Nutritional products for various animals.', 'images/category_image/animal_health_care.jpg'),
('Dairy Hygiene and Shed Supplies', NULL, 'Hygiene products for dairy operations.', 'images/category_image/niuniu.jpg'),
('Calving', NULL, 'Products to assist with animal birthing.', 'images/category_image/calving.jpg'),
('Animal Equipment', NULL, 'Equipment used in animal farming.', 'images/category_image/animal_equipment.jpg'),
('Water', NULL, 'Water management supplies.', 'images/category_image/water.jpg'),
('Fencing', NULL, 'Materials and tools for fencing.', 'images/category_image/fence.jpg'),
('Clothing', NULL, 'Clothing for farm operations.', 'images/category_image/cloth.jpg'),
('Footwear', NULL, 'Durable footwear for farming.', 'images/category_image/footwear.jpg'),
('Household Supplies', NULL, 'Supplies for rural households.', 'images/category_image/household_supplies.jpg'),
('Garden Supplies', NULL, 'Tools and materials for gardening.', 'images/category_image/garden_supplies.jpg'),
('Agrichemicals', NULL, 'Chemicals used in agriculture.', 'images/category_image/Agrichemicals.jpg'),
('Machinery & Oil', NULL, 'Machines and oils for agricultural use.', 'images/category_image/Machinery & Oil.jpg'),
('Pasture & Cropping', NULL, 'Products for pasture management and cropping.', 'images/category_image/Pasture & Cropping.jpg'),
('Fertilizer', NULL, 'Fertilizers for agricultural use.', 'images/category_image/Fertilizer.jpg'),
('Clearance', NULL, 'Discounted products on clearance.', 'images/category_image/Clearance.jpg');

-- Inserting sub-categories for 'Animal Health Care'

-- INSERT INTO categories (name, parent_id, description, ct_image_path) VALUES
-- ('Vaccines', 1, 'Vaccines to prevent diseases in animals.', '#'),
-- ('Antibiotics', 1, 'Antibiotics to treat animal diseases.', '#');


INSERT INTO products (category_id, name, description, price, pd_image_path, is_active) VALUES
(8, 'shirt', 't shirt', 12.00, 'product1.webp', 1),
(8, 'hat', 'hat', 22.00, 'product2.webp', 1);




