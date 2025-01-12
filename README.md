Shopback


This is our product that we have designed as an extension to the current shopback platform.
    Our extension being the digitalised stampcards and the social platform on our extension.
    
 To run our website on your local device(Our database is a locally hosted ) for testing and vreviewing.

1. Go to Mysql create a database 
2. Once db is created, key in the following query : 
                                                    USE mydb;

                                                    -- Step 1: Create users table
                                                    CREATE TABLE users (
                                                        user_id INT AUTO_INCREMENT PRIMARY KEY,
                                                        name VARCHAR(255),
                                                        highestShopbackPercent FLOAT,
                                                        numberOfVouchersUsed INT,
                                                        numberOfFriends INT,
                                                        ranking INT,
                                                        username VARCHAR(255) UNIQUE,
                                                        password VARCHAR(255)
                                                    );

                                                    -- Step 2: Create deals table
                                                    CREATE TABLE deals (
                                                        deal_id INT AUTO_INCREMENT PRIMARY KEY,
                                                        title VARCHAR(255),
                                                        description TEXT,
                                                        discount FLOAT,
                                                        valid_until DATE
                                                    );

                                                    -- Step 3: Create groups table
                                                    CREATE TABLE `groups` (
                                                        group_id INT AUTO_INCREMENT PRIMARY KEY,
                                                        deal_id INT NOT NULL,
                                                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                                        FOREIGN KEY (deal_id) REFERENCES deals(deal_id) ON DELETE CASCADE
                                                    );

                                                    -- Step 4: Create activities table
                                                    CREATE TABLE activities (
                                                        activity_id INT AUTO_INCREMENT PRIMARY KEY,
                                                        user_id INT NOT NULL,
                                                        store_name VARCHAR(255),
                                                        item_bought VARCHAR(255),
                                                        voucher_used VARCHAR(255),
                                                        date DATE,
                                                        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                                                    );

                                                    -- Step 5: Create group_members table
                                                    CREATE TABLE group_members (
                                                        member_id INT AUTO_INCREMENT PRIMARY KEY,
                                                        group_id INT NOT NULL,
                                                        user_id INT NOT NULL,
                                                        FOREIGN KEY (group_id) REFERENCES `groups`(group_id) ON DELETE CASCADE,
                                                        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                                                    );

                                                    -- Step 6: Create friends table
                                                    CREATE TABLE friends (
                                                        user_id_1 INT NOT NULL,
                                                        user_id_2 INT NOT NULL,
                                                        PRIMARY KEY (user_id_1, user_id_2),
                                                        FOREIGN KEY (user_id_1) REFERENCES users(user_id) ON DELETE CASCADE,
                                                        FOREIGN KEY (user_id_2) REFERENCES users(user_id) ON DELETE CASCADE
                                                    );

                                                    -- Step 7: Create user_store_purchases table
                                                    CREATE TABLE user_store_purchases (
                                                        id INT AUTO_INCREMENT PRIMARY KEY,
                                                        user_id INT NOT NULL,
                                                        store_1 INT DEFAULT 0,
                                                        store_2 INT DEFAULT 0,
                                                        store_3 INT DEFAULT 0,
                                                        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                                                    );

                                                    -- Step 8: Create discounts table
                                                    CREATE TABLE discounts (
                                                        id INT AUTO_INCREMENT PRIMARY KEY,
                                                        shopback_VoucherQty INT DEFAULT 0, 
                                                        store_1_VoucherQty INT DEFAULT 0,
                                                        store_2_VoucherQty INT DEFAULT 0,
                                                        store_3_VoucherQty INT DEFAULT 0,
                                                        user_id INT NOT NULL,
                                                        user_store_purchase_id INT NOT NULL,
                                                        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                                                        FOREIGN KEY (user_store_purchase_id) REFERENCES user_store_purchases(id) ON DELETE CASCADE
                                                    );

3. To key in some sample users: 
                         *You can try insert ur own sample users but here is what we used
                        
                        INSERT INTO users (name, highestShopbackPercent, numberOfVouchersUsed, numberOfFriends, ranking, username, password)
                        VALUES
                        ('John Doe', 15.5, 3, 5, 1, 'johndoe', 'password123'),
                        ('Jane Smith', 20.0, 5, 10, 2, 'janesmith', 'password456'),
                        ('Alice Brown', 10.2, 2, 8, 3, 'alicebrown', 'password789')
                        INSERT INTO activities (user_id, store_name, item_bought, voucher_used, date)
                        VALUES
                        (1, 'Store A', 'Smartphone', 'Voucher123', '2025-01-10'),
                        (2, 'Store B', 'Laptop', 'Voucher456', '2025-01-09'),
                        (3, 'Store C', 'Headphones', 'Voucher789', '2025-01-08');
                        INSERT INTO `groups` (deal_id)
                        VALUES
                        (1), 
                        (2), 
                        (3);
                        INSERT INTO deals (title, description, discount, valid_until)
                        VALUES
                        ('Deal A', 'Buy one get one free on all items', 50.0, '2025-02-01'),
                        ('Deal B', '20% off on electronics', 20.0, '2025-01-31'),
                        ('Deal C', 'Free shipping for orders above $50', 0.0, '2025-03-15');
                        INSERT INTO user_store_purchases (user_id, store_1, store_2, store_3)
                        VALUES
                        (1, 2, 3, 1),
                        (2, 0, 1, 2),
                        (3, 5, 0, 1);
                        INSERT INTO friends (user_id_1, user_id_2)
                        VALUES
                        (1, 2), 
                        (1, 3), 
                        (2, 3)
                        INSERT INTO discounts (shopback_VoucherQty, store_1_VoucherQty, store_2_VoucherQty, store_3_VoucherQty, user_id, user_store_purchase_id)
                        VALUES
                        (3, 2, 1, 0, 1, 2),
                        (2, 1, 0, 3, 2, 3),
                        (1, 0, 2, 1, 3, 4);
                        INSERT INTO group_members (group_id, user_id)
                        VALUES
                        (1, 1), 
                        (1, 2), 
                        (2, 3), 
                        (3, 1);


                        *user_id might differ from mine if so make the neccessary changes (as the user_id is auto incremented)


4. Update the username, password and database name with accordance to what u have set them to be in the app.py file (line: 11- 14 )



