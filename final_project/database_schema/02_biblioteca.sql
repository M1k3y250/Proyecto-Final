DROP DATABASE IF EXISTS gestor_biblioteca;
CREATE DATABASE gestor_biblioteca CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE gestor_biblioteca;

CREATE TABLE role (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(64) UNIQUE
);

CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) UNIQUE,
    email VARCHAR(120) UNIQUE,
    password_hash VARCHAR(256),
    role_id INT,
    FOREIGN KEY (role_id) REFERENCES role(id)
);

CREATE TABLE libro (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    isbn VARCHAR(20) UNIQUE,
    fecha_publicacion DATE,
    genero TEXT,
    disponibilidad BOOLEAN DEFAULT TRUE,
    user_id INTEGER REFERENCES user(id)
);

INSERT INTO role (name) VALUES ('Admin'), ('Bibliotecario'), ('Lector');
