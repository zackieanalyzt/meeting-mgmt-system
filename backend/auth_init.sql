-- MariaDB initialization script for Authentication Database
-- This script will be executed when the container starts for the first time

USE authdb;

-- Create users table for authentication (MD5 based as per spec)
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(32) NOT NULL, -- MD5 hash
    fullname VARCHAR(100),
    department VARCHAR(100),
    email VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert sample users for testing (password is MD5 hash of 'password123')
INSERT INTO users (username, password_hash, fullname, department, email) VALUES
('admin', '482c811da5d5b4bc6d497ffa98491e38', 'ผู้ดูแลระบบ', 'IT', 'admin@hospital.local'),
('user1', '482c811da5d5b4bc6d497ffa98491e38', 'นายสมชาย ใจดี', 'การพยาบาล', 'somchai@hospital.local'),
('user2', '482c811da5d5b4bc6d497ffa98491e38', 'นางสาวมาลี สวยงาม', 'เภสัชกรรม', 'malee@hospital.local')
ON DUPLICATE KEY UPDATE username=username;

-- Create indexes for performance
CREATE INDEX idx_username ON users(username);
CREATE INDEX idx_active ON users(is_active);