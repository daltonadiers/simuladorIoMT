-- Type for validate sex
CREATE TYPE tp_sex AS ENUM('M', 'F');

-- Users table
CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	name VARCHAR(50) NOT NULL,
    birth DATE NOT NULL,
    sex tp_sex NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    active BOOLEAN DEFAULT TRUE NOT NULL
);