-- PostgreSQL initialization script for Meeting Management System
-- This script will be executed when the container starts for the first time

-- Create database if not exists (handled by POSTGRES_DB env var)
-- CREATE DATABASE IF NOT EXISTS meeting_mgmt;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create full-text search configuration for Thai language
-- This will help with search functionality
CREATE TEXT SEARCH CONFIGURATION thai (COPY = simple);

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE meeting_mgmt TO postgres;