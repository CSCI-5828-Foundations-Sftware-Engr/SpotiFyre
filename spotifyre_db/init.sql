/*DROP DATABASE IF EXISTS spotifyre_db WITH (FORCE); */
CREATE DATABASE spotifyre_db;

\c spotifyre_db;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL
);
