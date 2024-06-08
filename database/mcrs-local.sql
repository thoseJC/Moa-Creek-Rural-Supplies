DROP TABLE IF EXISTS gift_card;
DROP VIEW IF EXISTS user_account_management;
DROP TABLE IF EXISTS line_item;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS conversations;
DROP TABLE IF EXISTS messages; 
DROP TABLE IF EXISTS shipments;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS receipt;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS payment;
DROP TABLE IF EXISTS address;
DROP TABLE IF EXISTS news;
DROP TABLE IF EXISTS notifications;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS user_roles;
DROP TABLE IF EXISTS promotions;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS shipping_fee;



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
    shipping_type ENUM('standard', 'oversize', 'pickup') DEFAULT 'standard',
    discount DECIMAL(5, 2) DEFAULT 0.00,
    discounted_price DECIMAL(10, 2) NULL,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE CASCADE
);

CREATE TABLE inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    quantity INT DEFAULT 0,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
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
    credit_limit decimal(10,2),
    credit_remaining decimal(10,2),
    credit_apply decimal(10,2),
	account_holder ENUM('init', 'apply', 'approve', 'decline') DEFAULT 'init',
	business_name VARCHAR(255),
	tax_employer_number VARCHAR(50),
	credit_check BOOLEAN,
    status BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (role_id) REFERENCES user_roles(role_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE address (
    address_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    street_address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


CREATE TABLE payment (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL ,
    total decimal(10,2) NOT NULL,
    payment_type VARCHAR(20),
    GST decimal(10,2) NOT NULL,
    freight DECIMAL(10,2),
    paid_date timestamp DEFAULT  CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE shipping_fee (
    shipping_fee_id INT AUTO_INCREMENT PRIMARY KEY,
    shipping_type ENUM('standard', 'oversized', 'pickup') NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

INSERT INTO shipping_fee (shipping_type, price) VALUES
('standard', 10.00),
('oversized', 100.00),
('pickup', 0.00);

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY key,
    user_id VARCHAR(36) not null,
    payment_id INT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10, 2) NOT NULL,
    GST decimal(10,2) NOT NULL,
    freight DECIMAL(10,2),
    status ENUM('pending', 'shipped', 'delivered', 'cancelled', 'ready_for_pickup') DEFAULT 'pending',
	shipping_fee_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (payment_id) REFERENCES payment (payment_id),
	FOREIGN KEY (shipping_fee_id) REFERENCES shipping_fee(shipping_fee_id)
);

CREATE TABLE order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    qty INT,
    price_per_unit DECIMAL(10, 2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE receipt(
    rcpt_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id varchar(36) not NULL,
    GST DECIMAL(10,2) not NULL,
    freight DECIMAL(10,2),
    total DECIMAL(10,2) NOT NULL,
    rcpt_date timestamp DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE line_item(
    lit_id INT AUTO_INCREMENT PRIMARY KEY,
    rcpt_id INT,
    product_id INT,
    lit_qty INT,
    lit_price DECIMAL(10,2),
    FOREIGN KEY (rcpt_id ) REFERENCES receipt(rcpt_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id varchar(36) NOT NULL,
    receiver_id varchar(36) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('sent', 'read') DEFAULT 'sent',
    FOREIGN KEY (sender_id) REFERENCES users(user_id),
    FOREIGN KEY (receiver_id) REFERENCES users(user_id)
);

CREATE TABLE conversations (
    conversation_id INT AUTO_INCREMENT PRIMARY KEY,
    staff_id varchar(36) NOT NULL,
    customer_id varchar(36) NOT NULL,
    last_message_id INT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES users(user_id),
    FOREIGN KEY (staff_id) REFERENCES users(user_id),
    FOREIGN KEY (last_message_id) REFERENCES messages(message_id)
);


CREATE TABLE shipments (
    shipment_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    shipping_type ENUM('standard', 'oversized', 'pickup', 'quote') DEFAULT 'standard',
    status ENUM('pending', 'shipped', 'delivered', 'cancelled', 'ready_for_pickup') DEFAULT 'pending',
    freight DECIMAL(10, 2),
    expected_delivery_date DATE,
    actual_delivery_date DATE,
    carrier_name VARCHAR(255),
    additional_info TEXT,  -- For any additional details like pickup instructions or freight forwarding info
	shipping_fee_id INT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
	FOREIGN KEY (shipping_fee_id) REFERENCES shipping_fee(shipping_fee_id)
);

CREATE TABLE notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


CREATE TABLE promotions (
    promotion_id INT AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(500) NOT NULL,
    promotion_type VARCHAR(125) NOT NULL,
    threshold_value decimal (10, 2) NULL,
    discount_value decimal (10, 2) NULL,
    target_category_id INT NULL, 
    target_product_id INT NULL,
    foreign key (target_category_id) references categories (category_id),
    foreign key (target_product_id) references products (product_id)
);

CREATE TABLE news (
    news_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    created_by VARCHAR(36) NOT NULL,
    is_published BOOLEAN DEFAULT FALSE,
    published_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(user_id)
);

CREATE TABLE gift_card (
    gf_card_id varchar(36) UNIQUE PRIMARY KEY ,
    amount decimal(6,00),
    holder VARCHAR(36),
    expried_date DATE,
    FOREIGN KEY (holder) REFERENCES users(user_id)
);


INSERT INTO user_roles (role_name) VALUES ('manager'), ('customer'), ('admin'), ('staff');

INSERT INTO users (user_id, role_id, first_name, last_name, username, email, user_password, status) 
VALUES 
    (UUID(), (SELECT role_id FROM user_roles WHERE role_name = 'manager'), 'Monica', 'Briggs', 'manager', 'manager@manager.com', '123456', TRUE),
    (UUID(), (SELECT role_id FROM user_roles WHERE role_name = 'customer'), 'Forrest', 'Curtis', 'customer', 'kevin.li@lincolnuni.ac.nz', '123456', TRUE),
    (UUID(), (SELECT role_id FROM user_roles WHERE role_name = 'admin'), 'Basil', 'Parker', 'admin', 'admin@admin.com', '123456', TRUE),
    (UUID(), (SELECT role_id FROM user_roles WHERE role_name = 'staff'), 'Harley', 'Stephenson', 'staff', 'staff@staff.com', '123456', TRUE),
    (UUID(), (SELECT role_id FROM user_roles WHERE role_name = 'manager'), 'Alice', 'Johnson', 'alice', 'alice@manager.com', 'password', TRUE),
    (UUID(), (SELECT role_id FROM user_roles WHERE role_name = 'customer'), 'Bob', 'Smith', 'bob', 'bob@customer.com', 'password', TRUE),
    (UUID(), (SELECT role_id FROM user_roles WHERE role_name = 'staff'), 'Charlie', 'Brown', 'charlie', 'charlie@staff.com', 'password', TRUE),
    (UUID(), (SELECT role_id FROM user_roles WHERE role_name = 'staff'), 'David', 'Wilson', 'david', 'david@staff.com', 'password', TRUE),
    (UUID(), (SELECT role_id FROM user_roles WHERE role_name = 'customer'), 'Eva', 'Taylor', 'eva', 'eva@customer.com', 'password', TRUE);


INSERT INTO categories (name, parent_id, description, ct_image_path)
VALUES ('Animal Health Care', NULL, 'Products aimed at maintaining animal health.',
        'images/category_image/animal_healthcare.jpg'),
       ('Animal Feed & Nutrition', NULL, 'Nutritional products for various animals.',
        'images/category_image/animal_health_care.jpg'),
       ('Dairy Hygiene and Shed Supplies', NULL, 'Hygiene products for dairy operations.',
        'images/category_image/niuniu.jpg'),
       ('Calving', NULL, 'Products to assist with animal birthing.', 'images/category_image/calving.jpg'),
       ('Animal Equipment', NULL, 'Equipment used in animal farming.', 'images/category_image/animal_equipment.jpg'),
       ('Water', NULL, 'Water management supplies.', 'images/category_image/water.jpg'),
       ('Fencing', NULL, 'Materials and tools for fencing.', 'images/category_image/fence.jpg'),
       ('Clothing', NULL, 'Clothing for farm operations.', 'images/category_image/cloth.jpg'),
       ('Footwear', NULL, 'Durable footwear for farming.', 'images/category_image/footwear.jpg'),
       ('Household Supplies', NULL, 'Supplies for rural households.', 'images/category_image/household_supplies.jpg'),
       ('Garden Supplies', NULL, 'Tools and materials for gardening.', 'images/category_image/garden_supplies.jpg'),
       ('Agrichemicals', NULL, 'Chemicals used in agriculture.', 'images/category_image/Agrichemicals.jpg'),
       ('Machinery & Oil', NULL, 'Machines and oils for agricultural use.',
        'images/category_image/Machinery & Oil.jpg'),
       ('Pasture & Cropping', NULL, 'Products for pasture management and cropping.',
        'images/category_image/Pasture & Cropping.jpg'),
       ('Fertilizer', NULL, 'Fertilizers for agricultural use.', 'images/category_image/Fertilizer.jpg'),
       ('Gift-Card', NULL, 'Gift-Card', 'images/category_image/gift_card.jpg'),
       ('Clearance', NULL, 'Discounted products on clearance.', 'images/category_image/Clearance.jpg');

-- Inserting sub-categories for 'Animal Health Care'
INSERT INTO categories (name, parent_id, description, ct_image_path)
VALUES ('Vaccines', (SELECT category_id
                     FROM (SELECT category_id FROM categories WHERE name = 'Animal Health Care') AS derived_table),
        'Vaccines to prevent diseases in animals.', ''),
       ('Antibiotics', (SELECT category_id
                        FROM (SELECT category_id FROM categories WHERE name = 'Animal Health Care') AS derived_table),
        'Antibiotics to treat animal diseases.', ''),
       ('Supplements', (SELECT category_id
                        FROM (SELECT category_id FROM categories WHERE name = 'Animal Health Care') AS derived_table),
        'Supplements to enhance animal health.', ''),
       ('Poultry Feed', (SELECT category_id
                         FROM (SELECT category_id
                               FROM categories
                               WHERE name = 'Animal Feed & Nutrition') AS derived_table), 'Feed for poultry.', ''),
       ('Cattle Feed', (SELECT category_id
                        FROM (SELECT category_id
                              FROM categories
                              WHERE name = 'Animal Feed & Nutrition') AS derived_table), 'Feed for cattle.', ''),
       ('Pet Food', (SELECT category_id
                     FROM (SELECT category_id FROM categories WHERE name = 'Animal Feed & Nutrition') AS derived_table),
        'Food for pets.', ''),
       ('Feeding Equipment',
        (SELECT category_id FROM (SELECT category_id FROM categories WHERE name = 'Animal Equipment') AS derived_table),
        'Equipment used for feeding livestock.', ''),
       ('Milking Equipment',
        (SELECT category_id FROM (SELECT category_id FROM categories WHERE name = 'Animal Equipment') AS derived_table),
        'Equipment used for milking livestock.', ''),
       ('Pest Control',
        (SELECT category_id FROM (SELECT category_id FROM categories WHERE name = 'Agrichemicals') AS derived_table),
        'Products to control pests in crops.', ''),
       ('Herbicides',
        (SELECT category_id FROM (SELECT category_id FROM categories WHERE name = 'Agrichemicals') AS derived_table),
        'Chemical products to control unwanted plants.', ''),
       ('Fungicides',
        (SELECT category_id FROM (SELECT category_id FROM categories WHERE name = 'Agrichemicals') AS derived_table),
        'Chemical products to control fungi.', '');


INSERT INTO products (category_id, name, description, price, pd_image_path, is_active)
VALUES ((SELECT category_id FROM categories WHERE name = 'Animal Health Care'), 'Vitamin Supplement',
        'A supplement to enhance animal health.', 25.00, '', 1),
       ((SELECT category_id FROM categories WHERE name = 'Animal Feed & Nutrition'), 'Animal Feed',
        'High-quality feed for various animals.', 15.00, '', 1),
       ((SELECT category_id FROM categories WHERE name = 'Dairy Hygiene and Shed Supplies'), 'Dairy Cleaner',
        'Cleaner for dairy equipment.', 10.00, '', 1),
       ((SELECT category_id FROM categories WHERE name = 'Calving'), 'Calving Aid', 'Aid for assisting in calving.',
<<<<<<< Updated upstream
        30.00, 'calving-aid.jpg', 1),
=======
        30.00, '', 1),
>>>>>>> Stashed changes
       ((SELECT category_id FROM categories WHERE name = 'Animal Equipment'), 'Feeding Bottle',
        'Bottle for feeding young animals.', 5.00, '', 1),
       ((SELECT category_id FROM categories WHERE name = 'Vaccines'), 'Animal Vaccine',
        'A vaccine to prevent diseases in animals.', 30.00, '', 1),
       ((SELECT category_id FROM categories WHERE name = 'Antibiotics'), 'Animal Antibiotics',
        'Antibiotics to treat animal diseases.', 20.00, '', 1),
       ((SELECT category_id FROM categories WHERE name = 'Supplements'), 'Animal Supplement',
        'A supplement to enhance animal health.', 25.00, '', 1),
       ((SELECT category_id FROM categories WHERE name = 'Poultry Feed'), 'Poultry Feed', 'Feed for poultry.', 15.00,
        '#', 1),
       ((SELECT category_id FROM categories WHERE name = 'Cattle Feed'), 'Cattle Feed', 'Feed for cattle.', 18.00, '',
        1),
       ((SELECT category_id FROM categories WHERE name = 'Pet Food'), 'Pet Food', 'Food for pets.', 22.00, '', 1),
       ((SELECT category_id FROM categories WHERE name = 'Feeding Equipment'), 'Feeder',
        'Equipment used for feeding livestock.', 50.00, '', 1),
       ((SELECT category_id FROM categories WHERE name = 'Milking Equipment'), 'Milking Machine',
        'Equipment used for milking livestock.', 120.00, '', 1),
       ((SELECT category_id FROM categories WHERE name = 'Pest Control'), 'Pest Control Spray',
        'Products to control pests in crops.', 25.00, '', 1),
       ((SELECT category_id FROM categories WHERE name = 'Herbicides'), 'Herbicide',
        'Chemical products to control unwanted plants.', 15.00, '', 1),
       ((SELECT category_id FROM categories WHERE name = 'Fungicides'), 'Fungicide','Chemical products to control fungi.', 20.00, '', 1),
       ((select category_id from categories where name = 'Gift-Card'), 'Gift Card', 'Gift-Card', 100.00, '', 1);


INSERT INTO inventory (product_id, quantity)
VALUES ((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Vitamin Supplement' LIMIT 1) AS derived_table), 30),
       ((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Animal Feed' LIMIT 1) AS derived_table), 56),
       ((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Dairy Cleaner' LIMIT 1) AS derived_table), 10),
       ((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Calving Aid' LIMIT 1) AS derived_table),
        28),
       ((SELECT product_id
         FROM (SELECT product_id FROM products WHERE name = 'Feeding Bottle' LIMIT 1) AS derived_table), 20),
       ((SELECT product_id
         FROM (SELECT product_id FROM products WHERE name = 'Animal Vaccine' LIMIT 1) AS derived_table), 40),
       ((SELECT product_id
         FROM (SELECT product_id FROM products WHERE name = 'Animal Antibiotics' LIMIT 1) AS derived_table), 50),
       ((SELECT product_id
         FROM (SELECT product_id FROM products WHERE name = 'Animal Supplement' LIMIT 1) AS derived_table), 30),
       ((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Poultry Feed' LIMIT 1) AS derived_table),
        60),
       ((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Cattle Feed' LIMIT 1) AS derived_table), 80),
       ((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Pet Food' LIMIT 1) AS derived_table),70),
       ((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Feeder' LIMIT 1) AS derived_table), 20),
       ((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Milking Machine' LIMIT 1) AS derived_table), 15),
       ((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Pest Control Spray' LIMIT 1) AS derived_table), 45),
       ((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Herbicide' LIMIT 1) AS derived_table),55),
       ((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Fungicide' LIMIT 1) AS derived_table),35),
       ((select product_id FROM products where name = 'Gift Card'), 10000000);


INSERT INTO payment (user_id, total, payment_type, GST, freight)
VALUES ((SELECT user_id FROM users WHERE username = 'customer'), 138.00, 'Credit Card', 18.00, 0.00),
       ((SELECT user_id FROM users WHERE username = 'alice'), 100.00, 'Credit Card', 15.00, 5.00),
       ((SELECT user_id FROM users WHERE username = 'bob'), 200.00, 'PayPal', 20.00, 10.00),
       ((SELECT user_id FROM users WHERE username = 'charlie'), 150.00, 'Bank Transfer', 18.00, 7.00),
       ((SELECT user_id FROM users WHERE username = 'david'), 80.00, 'Credit Card', 10.00, 3.00),
       ((SELECT user_id FROM users WHERE username = 'eva'), 120.00, 'Debit Card', 16.00, 6.00);


INSERT INTO orders (user_id, payment_id, total, GST, freight, status) VALUES
    ((SELECT user_id FROM users WHERE username = 'customer'), 1, 138.00, 18.00, 0.00, 'Pending'),
    ((SELECT user_id FROM users WHERE username = 'alice'), 1, 100.00, 15.00, 5.00, 'shipped'),
    ((SELECT user_id FROM users WHERE username = 'bob'), 2, 200.00, 20.00, 10.00, 'pending'),
    ((SELECT user_id FROM users WHERE username = 'charlie'), 3, 150.00, 18.00, 7.00, 'delivered'),
    ((SELECT user_id FROM users WHERE username = 'david'), 4, 80.00, 10.00, 3.00, 'cancelled'),
    ((SELECT user_id FROM users WHERE username = 'eva'), 5, 120.00, 16.00, 6.00, 'ready_for_pickup');


INSERT INTO receipt (user_id, GST, freight, total) VALUES
    ((SELECT user_id FROM users WHERE username = 'customer'), 18.00, 0.00, 138.00),
    ((SELECT user_id FROM users WHERE username = 'alice'), 15.00, 5.00, 100.00),
    ((SELECT user_id FROM users WHERE username = 'bob'), 20.00, 10.00, 200.00),
    ((SELECT user_id FROM users WHERE username = 'charlie'), 18.00, 7.00, 150.00),
    ((SELECT user_id FROM users WHERE username = 'david'), 10.00, 3.00, 80.00),
    ((SELECT user_id FROM users WHERE username = 'eva'), 16.00, 6.00, 120.00);

INSERT INTO messages (sender_id, receiver_id, content) VALUES
((SELECT user_id FROM users WHERE username = 'customer'), (SELECT user_id FROM users WHERE username = 'staff'), 'Hello, this is a test message.');


SELECT LAST_INSERT_ID() INTO @last_message_id;

INSERT INTO conversations (staff_id,customer_id, last_message_id) VALUES
((SELECT user_id FROM users WHERE username = 'staff'), (SELECT user_id FROM users WHERE username = 'customer'), @last_message_id);



INSERT INTO promotions ( description, promotion_type, threshold_value, discount_value, target_category_id, target_product_id) VALUES
('Buy two get one free', 'get_1_free', 2, NULL, 1, NULL),
('30% Discount', 'special_price', NULL, 0.30, 2, NULL),
('Buy 100 get delivery free', 'free_delivery', 100, NULL, NULL, NULL);

INSERT INTO address (user_id, street_address, city, state, postal_code, country, is_primary) VALUES
((SELECT user_id FROM users WHERE username = 'alice'), '123 Main St', 'Townsville', 'State1', '12345', 'Country1', TRUE),
((SELECT user_id FROM users WHERE username = 'bob'), '456 Elm St', 'Village', 'State2', '67890', 'Country1', TRUE),
((SELECT user_id FROM users WHERE username = 'charlie'), '789 Oak St', 'City', 'State3', '11223', 'Country1', TRUE),
((SELECT user_id FROM users WHERE username = 'david'), '101 Pine St', 'Metropolis', 'State4', '44556', 'Country1', TRUE),
((SELECT user_id FROM users WHERE username = 'eva'), '202 Maple St', 'Hamlet', 'State5', '77889', 'Country1', TRUE);

INSERT INTO messages (sender_id, receiver_id, content) VALUES
((SELECT user_id FROM users WHERE username = 'customer'), (SELECT user_id FROM users WHERE username = 'staff'), 'Hello, this is a test message.');


SELECT LAST_INSERT_ID() INTO @last_message_id;
INSERT INTO conversations (staff_id, customer_id, last_message_id) VALUES
((SELECT user_id FROM users WHERE username = 'staff'), (SELECT user_id FROM users WHERE username = 'customer'), @last_message_id);

CREATE VIEW user_account_management  AS (
SELECT us.user_id, us.first_name, us.last_name, us.username, us.email, ur.role_name, IF(us.status = 1, 'Active', 'Inactive') as account_status FROM users us LEFT JOIN user_roles ur ON us.role_id = ur.role_id
);

INSERT INTO news (title,content,created_by,is_published,published_date) VALUES 
('Company Expansion','We are expanding our operations to new regions, bringing our products and services closer to you. \r\n\r\nStay tuned for updates!',(SELECT user_id FROM users WHERE username = 'manager'),1,'2024-05-25 14:28:40'),
('test2','dadfa\r\nasdf\r\n\r\n\r\nasdfasdfa',(SELECT user_id FROM users WHERE username = 'manager'),0,NULL),
('Special Offer for Customers','Avail of our limited-time special offer exclusively for our valued customers. Enjoy discounts and benefits on select products.',(SELECT user_id FROM users WHERE username = 'manager'),1,'2024-05-25 14:29:00'),
('New Product Launch','We are excited to announce the launch of our latest product line. \r\n\r\nExplore innovative features and enhanced performance!',(SELECT user_id FROM users WHERE username = 'manager'),1,'2024-05-25 14:28:15');

-- insert notification to customer 
INSERT INTO notifications
(user_id, message, is_read, created_at)
VALUES((select user_id FROM users WHERE username = 'customer'), 'hello world', 0, CURRENT_TIMESTAMP);

INSERT INTO shipments (order_id, shipping_type, status, freight, expected_delivery_date, actual_delivery_date, carrier_name, additional_info) VALUES
(1, 'standard', 'shipped', 5.00, '2023-06-01', '2023-06-05', 'Carrier1', 'Leave at the front door.'),
(2, 'oversized', 'pending', 10.00, '2023-06-02', NULL, 'Carrier2', 'Handle with care.'),
(3, 'pickup', 'delivered', 0.00, '2023-06-03', '2023-06-06', 'Carrier3', 'Customer will pick up.'),
(4, 'quote', 'cancelled', 3.00, '2023-06-04', NULL, 'Carrier4', 'Cancelled due to customer request.'),
(5, 'standard', 'ready_for_pickup', 6.00, '2023-06-05', NULL, 'Carrier5', 'Ready for pickup at the warehouse.');

INSERT INTO gift_card (gf_card_id, amount, holder) VALUES (
    '1234-abcd' , 100.00, (select user_id from users where username = 'customer')
);


-- Adding 5 products to each of 'Footerwear', 'Household Supplies', 'Animal Equipment' categories
INSERT INTO products (category_id, name, description, price, pd_image_path, is_active)
VALUES (
	(SELECT category_id FROM categories WHERE name = 'Footwear'),
	'Grisport Genoa Safety Boots',
	'The Grisport Genoa safety boot is a premium, durable slip-on boot with a high temperature outsole. Grisport Genoa ankle slip-on safety boot. Dakar leather upper. Steel anti-penetration and steel toecap. Anti-static, oil and chemical resistant, heat resistant nitrile sole to 300 degrees.',
	199.99,
	'grisport-genoa-safety-boots.jpeg',
	1
),
(
	(SELECT category_id FROM categories WHERE name = 'Footwear'),
	'John Bull Oryx Lace Up Boots',
	'Featuring the quick closure and simple release BOA® Fit system that provides custom comfort and easy access to get them on and off quickly. Revolutionary world-first CushionCore comfort technology combines two compounds of PU injected into the midsole providing superior shock absorption at the heel while also providing rebound at the forefront as you step. TPU outsole with aggressive self-clearing tread pattern providing superior grip, stability and abrasion resistance. Super cushioning Comf2Bull air flow footbed of soft PU that is also antibacterial and washable. Quick closure and simple release BOA® Fit system. Adjustable for a personalised fit. Broad fitting 200 joule impact resistant type 1 steel toe cap. Coolmax® lining fabric helps transport moisture away from your foot, through the fabric, where it can evaporate quickly.Extra heavy-duty heel guard and a TPU toe guard for extra scuff protection. L-Protection® non-metallic penetration resistant insoles resist penetration even by small diameter nails and other objects.',
	344.95,
	'john-bull-oryx-lace-up-boots.jpeg',
	1
),
(
	(SELECT category_id FROM categories WHERE name = 'Footwear'),
	'Boonies Overlander Gumboots',
	'Now featuring the NEW SOFT UPPER. From the Farm to the Mai Mai – get into them. Mens Gumboots for Duck Shooting, Hunting, Fishing. Now in soft 4 way stretch neoprene so you can roll them down. Seamless construction of the Boonies ‘Comfy As ‘foot bed’. Mud dispersion cleats on the outside. Unprecedented traction and comfort. Made from hardwearing solid rubber, with mud dispersion cleats. 1059g so lightweight 390mm Tall- 455mm calf (size 10)',
	189.50,
	'boonies-overlander-gumboots.jpeg',
	1
),
(
	(SELECT category_id FROM categories WHERE name = 'Footwear'),
	'John Bull Raptor II Boots',
	'A popular rural style, this all-rounder features revolutionary CushionCore technology. Revolutionary world-first CushionCore comfort technology combines two compounds of PU injected into the midsole, providing superior shock absorption at the heel while also providing rebound at the forefront as you step. Broad fitting 200 joule impact resistant type 1 steel toe cap. Super cushioning Comf2Bull air flow footbed of soft PU that is also antibacterial and washable. TPU outsole with aggressive self-clearing tread pattern providing superior grip, stability and abrasion resistance.',
	209.50,
	'john-bull-raptor-ii-boots.jpeg',
	1
),
(
	(SELECT category_id FROM categories WHERE name = 'Footwear'),
	'John Bull Cougar II Boots',
	'The Cougar has a bullbar to take the kicks plus revolutionary CushionCore technology for comfort. Revolutionary world-first CushionCore comfort technology combines two compounds of PU injected into the midsole, providing superior shock absorption at the heel while also providing rebound at the forefront as you step. Super cushioning Comf2Bull air flow footbed of soft PU that is also antibacterial and washable. Moulded PU bullbar. Broad fitting 200 joule impact resistant type 1 steel toe cap. TPU outsole with aggressive self-clearing tread pattern providing superior grip, stability and abrasion resistance.',
	209.50,
	'john-bull-cougar-ii-boots.jpeg',
	1
),

(
	(SELECT category_id FROM categories WHERE name = 'Household Supplies'),
	'Curved Squeegee With Handle',
	'Elevate your cleaning experience with this curved squeegee. This 5mm rubber squeegee ensures that moisture is move in the right direction without the trouble of overspill. The squeegee has a thick 5mm rubber head supported by a strong alloy frame.',
	76.95,
	'curved-squeegee-with-handle.jpeg',
	1
),
(
	(SELECT category_id FROM categories WHERE name = 'Household Supplies'),
	'Cheese Cloth Roll Small',
	'100% cotton Kottenette cloth in tube section for carcass covering also super soft for professional cleaning and polishing cloths. Superior Carcass Covering. Premium Cleaning and Polishing. Eco-Friendly and Sustainable. Versatile and Convenient',
	37.95,
	'cheese-cloth-roll-small.jpeg',
	1
),
(
	(SELECT category_id FROM categories WHERE name = 'Household Supplies'),
	'Hand Scrub Brush Plastic Back',
	'An ergonomic hand brush ideal for scrubbing greasy surfaces. An ergonomic hand brush suited for scrubbing and scouring hard surfaces. Suitable for use in hot water and performs at sub zero temperatures.',
	26.00,
	'hand-scrub-brush-plastic-back.jpeg',
	1
),
(
	(SELECT category_id FROM categories WHERE name = 'Household Supplies'),
	'Pindone Pellets Possum and Rat',
	'Pindone P&R is a first generation anticoagulant poison cereal based pellet and does not pose the same secondary poison risk as second generation anticoagulants.',
	63.95,
	'pindone-pellets-possum-and-rat.jpeg',
	1
),
(
	(SELECT category_id FROM categories WHERE name = 'Household Supplies'),
	'Baby Bottle Brush',
	'The 355mm long  x 50mm Baby bottle brush filled in nylon with a twisted handle and a fan tip suited to cleaning bottles.',
	15.50,
	'baby-bottle-brush.jpeg',
	1
),

(
	(SELECT category_id FROM categories WHERE name = 'Animal Equipment'),
	'Stallion Calfateria Fence',
	'A 12 teat open trough calf feeder 80L. Ideal for new born calves. Made of tough durable plastic with rounded edges
Easy to transport and clean. Supplied with steel brackets. Peach teats included. Easy to take off and ensure a hygienic clean. Easy clean screw in teats and caps. 3-year warranty on a feeder.',
	356.50,
	'stallion-calfateria-fence.jpeg',
	1
),
(
	(SELECT category_id FROM categories WHERE name = 'Animal Equipment'),
	'Meal Feeder Poly Cone',
	'Poly cone feeder, 55 kilograms. Made of impact resistant polyethylene that is tough, durable and designed to last, we have a full range of meal feeders for use in both pens and paddocks. Poly cone feeders come with optional bird skirts that will keep meal clean and dry.',
	634.00,
	'meal-feeder-poly-cone.jpeg',
	1
),
(
	(SELECT category_id FROM categories WHERE name = 'Animal Equipment'),
	'Milk Bar Calf Feeder',
	'The Milk Bar™ 6 is the top seller for farms feeding all year round. It creates the perfect group size for hutches and is the ideal feeder for using the Follow the Teat System. Such a lovely light feeder to handle but has exceptional durability. The feeders stack inside each other with teats fitted so you can carry four or five at a time. Easy to clean, easy to use and calves love its little ledge to make them feel secure. The Ezi Lock hooks lock onto any rail type up to 75mm and flip upside down after feeding. Fitted with Milk Bar™ Teats to reduce cross suckling.',
	209.50,
	'milk-bar-calf-feeder.jpeg',
	1
),
(
	(SELECT category_id FROM categories WHERE name = 'Animal Equipment'),
	'Milk Bar Calf Trainer Bottle',
	'Getting the first few feeds right are critical to the overall performance of the calf and the Trainer Bottle is a great tool to help you achieve this.',
	50.00,
	'milk-bar-calf-trainer-bottle.jpeg',
	1
),
(
	(SELECT category_id FROM categories WHERE name = 'Animal Equipment'),
	'Acto Pritchard Lamb Teat Yellow',
	'Acto Pritchard Lamb Teat Yellow. The ever popular Pritchard™ Screw on Lamb Teat has a flutter valve which lets air back into the bottle as the lamb is drinking.',
	5.75,
	'acto-pritchard-lamb-teat-yellow.jpeg',
	1
),
(
	(SELECT category_id FROM categories WHERE name = 'Clothing'),
	'360 Performance Mens Jacket',
	'Our 360 Performance Mens Jacket is designed to withstand the rigours of farming life and weekend recreation, keeping you dry and comfortable in the harshest of conditions.',
	230.99,
	'mens-jacket.png',
	1
),
(
	(SELECT category_id FROM categories WHERE name = 'Clothing'),
	'360 Mens Long Sleeve Overalls- Spruce',
	'The 360 Mens Long Sleeve Overalls are built for dairy farming. Durable and hard-wearing, this product will go the distance.',
	59.99,
	'mens-long-sleeve-overalls.png',
	1
),
(
	(SELECT category_id FROM categories WHERE name = 'Clothing'),
	'360 Mens Short Sleeve Overalls - Spruce',
	'The 360 Mens Short Sleeve Overalls are built for dairy farming. Durable and hard-wearing, this product will go the distance.',
	56.99,
	'mens-short-sleeve-overalls.png',
	1
),
(
	(SELECT category_id FROM categories WHERE name = 'Clothing'),
	'360 Dairy Shed Bib Overtrouser',
	'100% Waterproof, Ultra-high frequency double welded seams, Acid resistant, perfect for the Dairy shed.',
	159.99,
	'dairy-shed-bib-overtrouser.png',
	1
),
(
	(SELECT category_id FROM categories WHERE name = 'Clothing'),
	'Lynn River Hi Vis Safety D/N Vest',
	'Tail Feature, Reflective Tape, Complies with AS/NZS 4602.1:2011 - Class D/N.',
	14.99,
	'safty-vest.png',
	1
),
(
	(SELECT category_id FROM categories WHERE name = 'Garden Supplies'),
	'Living Earth Organic Compost - 40L',
	'When dug through your soil, it provides your plants with yummy nutrients, improves the soil moisture retention and also gives those all-important worms a place to hangout and do their thing.',
	17.99,
	'organic-compost.png',
	1
),
(
	(SELECT category_id FROM categories WHERE name = 'Garden Supplies'),
	'Living Earth More Than Garden Mix - 40L',
	'Another quality product from the Living Earth Recycled soil range. Perfect for all your garden needs and safe to directly plant into. 100% Weed Free.',
	19.99,
	'garden-mix.png',
	1
),
(
	(SELECT category_id FROM categories WHERE name = 'Garden Supplies'),
	'Fiskars Aluminium Hand Trowel',
	'Durable one piece hi strength aluminium Beveled edges Softouch cushioned grip.',
	19.99,
	'hand-trowel.png',
	1
),
(
	(SELECT category_id FROM categories WHERE name = 'Garden Supplies'),
	'Viking Ash Handled Digging Spade',
	'You will love using this full sized digging spade. The polished steel blade is sharp and easy to clean. Function and looks - a great garden tool.',
	119.99,
	'digging-spade.png',
	1
),
(
	(SELECT category_id FROM categories WHERE name = 'Garden Supplies'),
	'Sprayer Pressure 5/7L Hozelock',
	'HOZELOCK GARDEN PRESSURE SPRAYER 5L.',
	79.99,
	'sprayer-pressure.png',
	1
),
(
	(SELECT category_id FROM categories WHERE name = 'Agrichemicals'),
	'Nufarm SlugOut 10kg',
	'Bait for the control of slugs and snails, particularly in new crops.',
	96.99,
	'nufarm-slugout.png',
	1
),
(
	(SELECT category_id FROM categories WHERE name = 'Agrichemicals'),
	'Pestoff Rodent Block 3kg',
	'An effective highly palatable rodent bait to control rats and mice.',
	74.99,
	'pestoff.png',
	1
),
(
	(SELECT category_id FROM categories WHERE name = 'Agrichemicals'),
	'Nufarm Valdo 800WG 500g',
	'Formulated for post emergence control of broadleaf weeds in clover, lucerne, chicory, new and mature pasture and maize.',
	229.99,
	'valdo.png',
	1
),
(
	(SELECT category_id FROM categories WHERE name = 'Agrichemicals'),
	'Nufarm Crucial 15L',
	'Non-selective herbicide for weed control. 600g/L high strength liquid formulation powered by triple salt, triple surfactant technology.',
	231.99,
	'nufarm-crucial.png',
	1
),
(
	(SELECT category_id FROM categories WHERE name = 'Agrichemicals'),
	'Raid Auto Advanced Twin Refill',
	'Repels flies and crawling insects 24/7.  305g refill can last up to 7.5 weeks.',
	59.99,
	'raid-twin-refill.png',
	1
);




-- Adding inventory data for all 15 products above

INSERT INTO inventory (product_id, quantity)
VALUES ((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Grisport Genoa Safety Boots' LIMIT 1) AS derived_table), 10),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'John Bull Oryx Lace Up Boots' LIMIT 1) AS derived_table), 30),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Boonies Overlander Gumboots' LIMIT 1) AS derived_table), 50),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'John Bull Raptor II Boots' LIMIT 1) AS derived_table), 80),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'John Bull Cougar II Boots' LIMIT 1) AS derived_table), 100),

((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Curved Squeegee With Handle' LIMIT 1) AS derived_table), 10),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Cheese Cloth Roll Small' LIMIT 1) AS derived_table), 30),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Hand Scrub Brush Plastic Back' LIMIT 1) AS derived_table), 50),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Pindone Pellets Possum and Rat' LIMIT 1) AS derived_table), 80),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Baby Bottle Brush' LIMIT 1) AS derived_table), 100),

((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Stallion Calfateria Fence' LIMIT 1) AS derived_table), 10),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Meal Feeder Poly Cone' LIMIT 1) AS derived_table), 30),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Milk Bar Calf Feeder' LIMIT 1) AS derived_table), 50),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Milk Bar Calf Trainer Bottle' LIMIT 1) AS derived_table), 80),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Acto Pritchard Lamb Teat Yellow' LIMIT 1) AS derived_table), 100),

((SELECT product_id FROM (SELECT product_id FROM products WHERE name = '360 Performance Mens Jacket' LIMIT 1) AS derived_table), 50),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = '360 Mens Long Sleeve Overalls- Spruce' LIMIT 1) AS derived_table), 40),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = '360 Mens Short Sleeve Overalls - Spruce' LIMIT 1) AS derived_table), 40),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = '360 Dairy Shed Bib Overtrouser' LIMIT 1) AS derived_table), 50),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Lynn River Hi Vis Safety D/N Vest' LIMIT 1) AS derived_table), 50),

((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Living Earth Organic Compost - 40L' LIMIT 1) AS derived_table), 80),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Living Earth More Than Garden Mix - 40L' LIMIT 1) AS derived_table), 80),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Fiskars Aluminium Hand Trowel' LIMIT 1) AS derived_table), 100),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Viking Ash Handled Digging Spade' LIMIT 1) AS derived_table), 100),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Sprayer Pressure 5/7L Hozelock' LIMIT 1) AS derived_table), 80),

((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Nufarm SlugOut 10kg' LIMIT 1) AS derived_table), 50),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Pestoff Rodent Block 3kg' LIMIT 1) AS derived_table), 50),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Nufarm Valdo 800WG 500g' LIMIT 1) AS derived_table), 50),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Nufarm Crucial 15L' LIMIT 1) AS derived_table), 30),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Raid Auto Advanced Twin Refill' LIMIT 1) AS derived_table), 80);

