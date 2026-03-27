-- drug_spot_backend/schema.sql
-- PostgreSQL schema for Drug Spot backend

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(30),
    password_hash VARCHAR(255) NOT NULL,
    bio TEXT,
    avatar_path VARCHAR(255),
    user_type VARCHAR(20) NOT NULL CHECK (user_type IN ('pharmacy', 'patient'))
);

CREATE TABLE pharmacies (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    lat DOUBLE PRECISION NOT NULL,
    lng DOUBLE PRECISION NOT NULL,
    phone VARCHAR(30) NOT NULL,
    accent VARCHAR(10)
);

CREATE TABLE medicines (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DOUBLE PRECISION NOT NULL,
    pharmacy_id INTEGER NOT NULL REFERENCES pharmacies(id) ON DELETE CASCADE
);

CREATE TABLE medicine_requests (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    contact VARCHAR(50) NOT NULL,
    medicine_name VARCHAR(100) NOT NULL,
    avatar_path VARCHAR(255),
    use_asset BOOLEAN DEFAULT FALSE
);

-- Indexes for performance
CREATE INDEX idx_medicine_name ON medicines(name);
CREATE INDEX idx_pharmacy_name ON pharmacies(name);
