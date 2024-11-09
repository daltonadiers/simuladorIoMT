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

CREATE TABLE collected_data (
    seq SERIAL PRIMARY KEY,
    userid INTEGER REFERENCES users(id) ON DELETE CASCADE,
    datetime TIMESTAMP NOT NULL,
    type INTEGER,
    value1 FLOAT,
    value2 FLOAT,
    inhouse BOOLEAN
);
CREATE TABLE types (
    seq SERIAL PRIMARY KEY,
    userid INTEGER REFERENCES users(id) ON DELETE CASCADE,
    type INTEGER NOT NULL
);