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
	account_holder ENUM('init', 'applied', 'approved', 'declined') DEFAULT 'init',
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
    (UUID(), (SELECT role_id FROM user_roles WHERE role_name = 'manager'), 'Monica', 'Briggs', 'manager', 'manager@manager.com', '1', TRUE),
    (UUID(), (SELECT role_id FROM user_roles WHERE role_name = 'customer'), 'Forrest', 'Curtis', 'customer', 'kevin.li@lincolnuni.ac.nz', '1', TRUE),
    (UUID(), (SELECT role_id FROM user_roles WHERE role_name = 'admin'), 'Basil', 'Parker', 'admin', 'admin@admin.com', '1', TRUE),
    (UUID(), (SELECT role_id FROM user_roles WHERE role_name = 'staff'), 'Harley', 'Stephenson', 'staff', 'staff@staff.com', '1', TRUE),
    (UUID(), (SELECT role_id FROM user_roles WHERE role_name = 'manager'), 'Alice', 'Johnson', 'alice', 'alice@manager.com', '1', TRUE),
    (UUID(), (SELECT role_id FROM user_roles WHERE role_name = 'customer'), 'Bob', 'Smith', 'bob', 'bob@customer.com', '1', TRUE),
    (UUID(), (SELECT role_id FROM user_roles WHERE role_name = 'staff'), 'Charlie', 'Brown', 'charlie', 'charlie@staff.com', '1', TRUE),
    (UUID(), (SELECT role_id FROM user_roles WHERE role_name = 'staff'), 'David', 'Wilson', 'david', 'david@staff.com', '1', TRUE),
    (UUID(), (SELECT role_id FROM user_roles WHERE role_name = 'customer'), 'Eva', 'Taylor', 'eva', 'eva@customer.com', '1', TRUE);


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
VALUES ((SELECT category_id FROM categories WHERE name = 'Animal Health Care'), 'Equilibrium Mineral Mix',
        'Equilibrium Mineral Mix is an all in one vitamin and mineral supplement for horses that contains balanced ratios of vitamins, macro and trace minerals and salts (electrolytes).', 25.00, 'Mineral-Mix-5kg-web.png', 1),
       ((SELECT category_id FROM categories WHERE name = 'Animal Feed & Nutrition'), 'Calcium deficiency in cattle',
        'Instant release of calcium offers 26g per bolus of two different calcium sources – Calcium Phosphate and Calcium Formate.
Reduces the risk of milk fever by increasing the levels of calcium in the blood.', 15.00, 'Calcitop-new-web.png', 1),
       ((SELECT category_id FROM categories WHERE name = 'Dairy Hygiene and Shed Supplies'), 'Dairy Cleaner',
        'Cleaner for dairy equipment', 10.00, 'CleanerfordairyEquipment.jpeg', 1),
       ((SELECT category_id FROM categories WHERE name = 'Calving'), 'Calving Aid', 'Aid for assisting in calving.',
        30.00, '', 1),
       ((SELECT category_id FROM categories WHERE name = 'Animal Equipment'), 'Feeding Bottle','Bottle for feeding young animals.jpeg', 5.00, 'Feeding-Bottle.png', 1),
       ((SELECT category_id FROM categories WHERE name = 'Vaccines'), 'Animal Vaccine',
        'A vaccine to prevent diseases in animals.jpeg', 30.00, '', 1),
       ((SELECT category_id FROM categories WHERE name = 'Antibiotics'), 'Animal Antibiotics',
        'Antibiotics to treat animal diseases.jpeg', 20.00, '', 1),
       ((SELECT category_id FROM categories WHERE name = 'Supplements'), 'Animal Supplement',
        'A supplement to enhance animal health.jpeg', 25.00, '', 1),
       ((SELECT category_id FROM categories WHERE name = 'Poultry Feed'), 'Poultry Feed', 'Feed for poultry.', 15.00,
        '#', 1),
       ((SELECT category_id FROM categories WHERE name = 'Cattle Feed'), 'Cattle Feed', 'Feed for cattle.', 18.00, '',
        1),
       ((SELECT category_id FROM categories WHERE name = 'Pet Food'), 'Pet Food', 'Food for pets.', 22.00, '', 1),
       ((SELECT category_id FROM categories WHERE name = 'Feeding Equipment'), 'Feeder',
        'Equipment used for feeding livestock.jpeg', 50.00, '', 1),
       ((SELECT category_id FROM categories WHERE name = 'Milking Equipment'), 'Milking Machine',
        'Equipment used for milking livestock.jpeg', 120.00, '', 1),
       ((SELECT category_id FROM categories WHERE name = 'Pest Control'), 'Pest Control Spray',
        'Products to control pests in crops.jpeg', 25.00, '', 1),
       ((SELECT category_id FROM categories WHERE name = 'Herbicides'), 'Herbicide',
        'Chemical products to control unwanted plants.', 15.00, '', 1),
       ((SELECT category_id FROM categories WHERE name = 'Fungicides'), 'Fungicide','Chemical products to control fungi.', 20.00, '', 1),
       ((select category_id from categories where name = 'Gift-Card'), 'Gift Card 100', 'Gift-Card Value $100', 100.00, 'giftcard-100.png', 1),
       ((select category_id from categories where name = 'Gift-Card'), 'Gift Card 50', 'Gift-Card Value $50', 50.00, 'giftcard-50.png', 1),
       ((select category_id from categories where name = 'Gift-Card'), 'Gift Card 20', 'Gift-Card Value $20', 20.00, 'giftcard-20.png', 1),
        ((SELECT category_id FROM categories WHERE name = 'Dairy Hygiene and Shed Supplies'), 'Iodine-Tincture-Spray','Iodine Tincture Spray 10% contains free iodine (in alcohol) which has antiseptic qualities. This is the iodine best used on wounds ie dehorning wounds, navels on calves, sheep and horses, etc.', 55.00, 'Iodine-Tincture-Spray-10-1L-5L-web.jpeg', 1),
        ((SELECT category_id FROM categories WHERE name = 'Dairy Hygiene and Shed Supplies'),
        'Teatease Udder Cream for lactating cows',
        'Teatease Udder Cream for lactating cows is an odourless non staining udder cream with antiseptic qualities.',
        188.40,
        'Teatease-500g-web.png',
        1),
        ((SELECT category_id FROM categories WHERE name = 'Dairy Hygiene and Shed Supplies'), 'Hand Sanitiser Aerosol','Quick acting highly effective alcohol-based hand sanitiser.
Kills 99.99% of germs. Effective against a wide range of pathogens incl COVID-19.
Rapidly evaporates from hands.
Fragrance free.
Contains Benzalkonium Chloride (BAC) disinfectant to give additional sanitising power.
Contains an emollient to moisturise hands.
Disinfects hands when soap and water are not readily available.
', 24.95, 'Hand-sanitiser.jpeg', 1),
       ((SELECT category_id FROM categories WHERE name = 'Animal Feed & Nutrition'), 'Biostack AP Effluent Pond Management','The world’s first and only photosynthetic bacteria cultivated for use in unique formulations specifically for agricultural wastewater systems including effluent ponds.', 614.10, 'Biostack-4L-ap-web.png', 1),
       ((SELECT category_id FROM categories WHERE name = 'Animal Feed & Nutrition'), 'Turmericle Turmeric and Coconut Oil Powder','Turmericle Turmeric and Coconut Oil Powder is a unique powdered blend of well researched nutraceutical herbs including two varieties of turmeric, and black pepper. Combined with powdered coconut oil, this easy to feed powder is suitable for horses, and dogs.', 114.10, 'Turmericle-NZ-500g-round-Pail-web.png', 1),
       ((SELECT category_id FROM categories WHERE name = 'Animal Feed & Nutrition'), 'Calf Oral Electrolytes','Animal Health Direct Limited Calf Electrolyte is fast acting free flowing formulation of electrolyte salts easily dissolved in water. Designed to assist with treatment for calves which are scouring as a result of bacterial, viral or nutritional causes. Can also be used for lambs and goat kids.', 152.09, 'Calf-Oral-Electrolyte-Replacer-1.8kg-web.png', 1),
       ((SELECT category_id FROM categories WHERE name = 'Animal Feed & Nutrition'), 'Oral Mag','Smooth easy to drench formulation which can also be added to feed.Offers an extended residual effect meaning the magnesium is available when needed.', 828.14, 'Oral-Mag-2L-web.png', 1),
       ((SELECT category_id FROM categories WHERE name = 'Animal Feed & Nutrition'), 'MetaBoost 4 in 1 Metabolic Injection','Metabolic injection containing high levels of Calcium, Magnesium, Phosphorus and Dextrose. Effective in the treatment and prevention of milk fever and grass staggers.Flexible 500ml collapsible pouch with a unique snap off plug and 14 gauge monoject needle included.', 1028.14, 'Metaboost-4-in-1-green-web-1.png', 1),
       ((SELECT category_id FROM categories WHERE name = 'Animal Health Care'), 'AHD Medicated Shampoo Animal Wash','Cleans and protects your animal’s coat leaving it soft and shiny while promoting healthy skin. Showing off the best of your animal’s coat.Contains anti-bacterial and anti-fungal ingredients to suppress skin infections.', 46.14, 'Medicated-shampoo-500ml-web.png', 1),
       ((SELECT category_id FROM categories WHERE name = 'Animal Health Care'), 'AHD Zinc Ointment','Treats slight abrasions and minor wounds. Prevents sunburn in all species.', 58.82, 'Zinc-web.png', 1),
       ((SELECT category_id FROM categories WHERE name = 'Animal Health Care'), 'Equine Health Aloe Vera Gel','Contains Arnica and Manuka Honey. Aids in blood circulation to bruised areas.', 94.20, 'Aloe-Vera-Gel-web.png', 1),
        ((SELECT category_id FROM categories WHERE name = 'Dairy Hygiene and Shed Supplies'), 'Leader Rubber Rings','Leader Rubber Rings are a pure latex standard marking ring that have no fillings to ensure positive, germ-free marking and are used for the castration of lambs and calves.', 38.35, 'Leader-marker-rings-500-web.png', 1);

INSERT INTO inventory (product_id, quantity)
VALUES ((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Equilibrium Mineral Mix' LIMIT 1) AS derived_table), 30),
       ((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Calcium deficiency in cattle' LIMIT 1) AS derived_table), 56),
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
       ((select product_id FROM products where name = 'Iodine-Tincture-Spray'), 500),
       ((select product_id FROM products where name = 'Leader Rubber Rings'), 500),
       ((select product_id FROM products where name = 'Teatease Udder Cream for lactating cows'), 500),
       ((select product_id FROM products where name = 'Biostack AP Effluent Pond Management'), 500),
       ((select product_id FROM products where name = 'Calf Oral Electrolytes'), 500),
       ((select product_id FROM products where name = 'Oral Mag'), 500),
       ((select product_id FROM products where name = 'MetaBoost 4 in 1 Metabolic Injection'), 500),
       ((select product_id FROM products where name = 'AHD Medicated Shampoo Animal Wash'), 500),
       ((select product_id FROM products where name = 'AHD Zinc Ointment'), 500),
       ((select product_id FROM products where name = 'Equine Health Aloe Vera Gel'), 500),
       ((select product_id FROM products where name = 'Gift Card 100'), 500),
       ((select product_id FROM products where name = 'Gift Card 50'), 500),
       ((select product_id FROM products where name = 'Gift Card 20'), 500),
       ((select product_id FROM products where name = 'Hand Sanitiser Aerosol'), 500);

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


CREATE VIEW user_account_management  AS (
SELECT us.user_id, us.first_name, us.last_name, us.username, us.email, ur.role_name, IF(us.status = 1, 'Active', 'Inactive') as account_status FROM users us LEFT JOIN user_roles ur ON us.role_id = ur.role_id
);

INSERT INTO news (title,content,created_by,is_published,published_date) VALUES 
('Company Expansion','We are expanding our operations to new regions, bringing our products and services closer to you. \r\n\r\nStay tuned for updates!',(SELECT user_id FROM users WHERE username = 'manager'),1,'2024-05-25 14:28:40'),
('test2','dadfa\r\nasdf\r\n\r\n\r\nasdfasdfa',(SELECT user_id FROM users WHERE username = 'manager'),0,NULL),
('Special Offer for Customers','Avail of our limited-time special offer exclusively for our valued customers. Enjoy discounts and benefits on select products.',(SELECT user_id FROM users WHERE username = 'manager'),1,'2024-05-25 14:29:00'),
('New Product Launch','We are excited to announce the launch of our latest product line. \r\n\r\nExplore innovative features and enhanced performance!',(SELECT user_id FROM users WHERE username = 'manager'),1,'2024-05-25 14:28:15');

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

--  Machinery & Oil
INSERT INTO products (category_id, name, description, price, pd_image_path, is_active)
VALUES
((SELECT category_id FROM categories WHERE name = 'Machinery & Oil'), 'Tractor Oil', 'High performance tractor oil.', 100.00, 'tractor_oil.jpg', 1),
((SELECT category_id FROM categories WHERE name = 'Machinery & Oil'), 'Hydraulic Fluid', 'Hydraulic fluid for various machinery.', 75.00, 'hydraulic_fluid.jpg', 1),
((SELECT category_id FROM categories WHERE name = 'Machinery & Oil'), 'Engine Oil', 'Premium engine oil.', 50.00, 'engine_oil.jpg', 1),
((SELECT category_id FROM categories WHERE name = 'Machinery & Oil'), 'Gear Oil', 'Gear oil for smooth operation.', 80.00, 'gear_oil.jpg', 1),
((SELECT category_id FROM categories WHERE name = 'Machinery & Oil'), 'Transmission Fluid', 'Transmission fluid for heavy-duty machinery.', 90.00, 'transmission_fluid.jpg', 1);

INSERT INTO products (category_id, name, description, price, pd_image_path, is_active)
VALUES
((SELECT category_id FROM categories WHERE name = 'Pasture & Cropping'), 'Pasture Seed Mix', 'High-quality seed mix for pasture.', 150.00, 'pasture_seed_mix.jpg', 1),
((SELECT category_id FROM categories WHERE name = 'Pasture & Cropping'), 'Crop Fertilizer', 'Fertilizer for better crop yield.', 120.00, 'crop_fertilizer.jpg', 1),
((SELECT category_id FROM categories WHERE name = 'Pasture & Cropping'), 'Herbicide', 'Herbicide for weed control.', 60.00, 'Herbicide.jpg', 1),
((SELECT category_id FROM categories WHERE name = 'Pasture & Cropping'), 'Pesticide', 'Pesticide for crop protection.', 70.00, 'pesticide.jpg', 1),
((SELECT category_id FROM categories WHERE name = 'Pasture & Cropping'), 'Growth Enhancer', 'Enhancer for crop growth.', 90.00, 'growth_enhancer.jpg', 1);

INSERT INTO products (category_id, name, description, price, pd_image_path, is_active)
VALUES
((SELECT category_id FROM categories WHERE name = 'Fertilizer'), 'Organic Fertilizer', 'Organic fertilizer for healthy crops.', 110.00, 'organic_fertilizer.jpg', 1),
((SELECT category_id FROM categories WHERE name = 'Fertilizer'), 'Nitrogen Fertilizer', 'Nitrogen-rich fertilizer.', 130.00, 'nitrogen_fertilizer.jpg', 1),
((SELECT category_id FROM categories WHERE name = 'Fertilizer'), 'Phosphate Fertilizer', 'Phosphate fertilizer for strong roots.', 140.00, 'phosphate_fertilizer.jpg', 1),
((SELECT category_id FROM categories WHERE name = 'Fertilizer'), 'Potassium Fertilizer', 'Potassium fertilizer for plant vigor.', 150.00, 'potassium_fertilizer.jpg', 1),
((SELECT category_id FROM categories WHERE name = 'Fertilizer'), 'Liquid Fertilizer', 'Liquid fertilizer for easy application.', 160.00, 'liquid_fertilizer.jpg', 1);

INSERT INTO products (category_id, name, description, price, pd_image_path, is_active)
VALUES
((SELECT category_id FROM categories WHERE name = 'Clearance'), 'Discounted Seed Mix', 'Seed mix at a discounted price.', 50.00, 'discounted_seed_mix.jpg', 1),
((SELECT category_id FROM categories WHERE name = 'Clearance'), 'Clearance Pesticide', 'Pesticide at a clearance price.', 40.00, 'clearance_pesticide.jpg', 1),
((SELECT category_id FROM categories WHERE name = 'Clearance'), 'Clearance Fertilizer', 'Fertilizer at a clearance price.', 60.00, 'clearance_fertilizer.jpg', 1),
((SELECT category_id FROM categories WHERE name = 'Clearance'), 'Clearance Herbicide', 'Herbicide at a clearance price.', 30.00, 'clearance_herbicide.jpg', 1),
((SELECT category_id FROM categories WHERE name = 'Clearance'), 'Clearance Equipment', 'Equipment at a clearance price.', 70.00, 'clearance_equipment.jpg', 1);

INSERT INTO inventory (product_id, quantity)
VALUES
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Tractor Oil' LIMIT 1) AS derived_table), 100),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Hydraulic Fluid' LIMIT 1) AS derived_table), 120),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Engine Oil' LIMIT 1) AS derived_table), 140),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Gear Oil' LIMIT 1) AS derived_table), 160),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Transmission Fluid' LIMIT 1) AS derived_table), 180),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Pasture Seed Mix' LIMIT 1) AS derived_table), 200),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Crop Fertilizer' LIMIT 1) AS derived_table), 220),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Herbicide' LIMIT 1) AS derived_table), 240),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Pesticide' LIMIT 1) AS derived_table), 260),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Growth Enhancer' LIMIT 1) AS derived_table), 280),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Organic Fertilizer' LIMIT 1) AS derived_table), 300),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Nitrogen Fertilizer' LIMIT 1) AS derived_table), 320),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Phosphate Fertilizer' LIMIT 1) AS derived_table), 340),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Potassium Fertilizer' LIMIT 1) AS derived_table), 360),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Liquid Fertilizer' LIMIT 1) AS derived_table), 380),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Discounted Seed Mix' LIMIT 1) AS derived_table), 400),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Clearance Pesticide' LIMIT 1) AS derived_table), 420),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Clearance Fertilizer' LIMIT 1) AS derived_table), 440),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Clearance Herbicide' LIMIT 1) AS derived_table), 460),
((SELECT product_id FROM (SELECT product_id FROM products WHERE name = 'Clearance Equipment' LIMIT 1) AS derived_table), 480);


