CREATE DATABASE IF NOT EXISTS testdb;

USE testdb;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    credit_card_number VARCHAR(100) NOT NULL
);

INSERT INTO users (name, email, credit_card_number) VALUES
('Alice',
 'alice@example.com',
 '1234-5678-9012-3454'),
('Bob',
 'bob@example.com',
 '1234-5678-9012-3456'
 );


CREATE TABLE IF NOT EXISTS users_ips (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    ip_address VARCHAR(100) NOT NULL
);

INSERT INTO users_ips (user_id, ip_address) VALUES
(1,
 '127.0.0.1'),
(2,
 '127.0.0.2');