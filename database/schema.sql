CREATE DATABASE IF NOT EXISTS taximeter;
USE taximeter;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL
);

INSERT INTO users (username, password, role) 
VALUES ('admin', 'admin123', 'admin'); 