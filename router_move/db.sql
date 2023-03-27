DROP DATABASE IF EXISTS RouterMove;
CREATE DATABASE RouterMove;
USE RouterMove;

CREATE TABLE devices (
	name VARCHAR(40) PRIMARY KEY,
	ip VARCHAR(25),
	user_name VARCHAR(20),
	users_passwd VARCHAR(50)
);

INSERT INTO	devices (ip, name, user_name, users_passwd)
VALUES
('192.168.168.254', 'first', 'api1', 'NpBp0205'),
('192.168.169.254', 'second', 'api1', 'NpBp0205');

CREATE TABLE users (
	name VARCHAR(15) PRIMARY KEY,
	passwd VARCHAR(20)
);

INSERT INTO users
VALUES
('admin', 'parallaxtall');