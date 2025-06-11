CREATE DATABASE PDC;

-- Crear tablas de geografía
CREATE TABLE pais (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE departamento (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    id_pais INT REFERENCES pais(id)
);

CREATE TABLE municipio (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    id_departamento INT REFERENCES departamento(id)
);

-- Crear tabla de empresas
CREATE TABLE empresa (
    id SERIAL PRIMARY KEY,
    id_pais INT REFERENCES pais(id),
    id_departamento INT REFERENCES departamento(id),
    id_municipio INT REFERENCES municipio(id),
    nit VARCHAR(50) NOT NULL,
    razon_social VARCHAR(100),
    nombre_comercial VARCHAR(100),
    telefono VARCHAR(50),
    correo VARCHAR(100)
);

-- Crear tabla de colaboradores
CREATE TABLE colaborador (
    id SERIAL PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    edad INT,
    telefono VARCHAR(50),
    correo VARCHAR(100)
);

-- Relación N a N (si activas la opción de múltiples empresas)
CREATE TABLE empresa_colaborador (
    id SERIAL PRIMARY KEY,
    id_empresa INT REFERENCES empresa(id) ON DELETE CASCADE,
    id_colaborador INT REFERENCES colaborador(id) ON DELETE CASCADE
);

-- Insertar datos de ejemplo
INSERT INTO pais(nombre) VALUES ('Guatemala');
INSERT INTO departamento (nombre, id_pais) VALUES
('Alta Verapaz', 1),
('Baja Verapaz', 1),
('Chimaltenango', 1),
('Chiquimula', 1),
('El Progreso', 1),
('Escuintla', 1),
('Guatemala', 1),
('Huehuetenango', 1),
('Izabal', 1),
('Jalapa', 1),
('Jutiapa', 1),
('Petén', 1),
('Quetzaltenango', 1),
('Quiché', 1),
('Retalhuleu', 1),
('Sacatepéquez', 1),
('San Marcos', 1),
('Santa Rosa', 1),
('Sololá', 1),
('Suchitepéquez', 1),
('Totonicapán', 1),
('Zacapa', 1);

INSERT INTO municipio (nombre, id_departamento) VALUES
('Chahal', 1),
('Chisec', 1),
('Cobán', 1),
('Fray Bartolomé de las Casas', 1),
('La Tinta', 1),
('Lanquín', 1),
('Panzós', 1),
('Raxruhá', 1),
('San Cristóbal Verapaz', 1),
('San Juan Chamelco', 1),
('San Pedro Carchá', 1),
('Santa Cruz Verapaz', 1),
('Santa María Cahabón', 1),
('Senahú', 1),
('Tamahú', 1),
('Tactic', 1);

INSERT INTO municipio (nombre, id_departamento) VALUES
('Amatitlán', 7),
('Chinautla', 7),
('Chuarrancho', 7),
('Ciudad de Guatemala', 7),
('Fraijanes', 7),
('Mixco', 7),
('Palencia', 7),
('San José del Golfo', 7),
('San José Pinula', 7),
('San Juan Sacatepéquez', 7),
('San Miguel Petapa', 7),
('San Pedro Ayampuc', 7),
('San Pedro Sacatepéquez', 7),
('San Raymundo', 7),
('Santa Catarina Pinula', 7),
('Villa Canales', 7),
('Villa Nueva', 7);


INSERT INTO empresa(id_pais, id_departamento, id_municipio, nit, razon_social, nombre_comercial, telefono, correo)
VALUES (1, 7, 4, '1234567-8', 'Empresa S.A.', 'Empresa GT', '12345678', 'info@empresa.com');

INSERT INTO colaborador(nombre_completo, edad, telefono, correo)
VALUES ('Juan Pérez', 30, '98765432', 'juan@correo.com');

INSERT INTO empresa_colaborador(id_empresa, id_colaborador) VALUES (1, 1);
