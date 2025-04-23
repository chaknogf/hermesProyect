-- Crear base de datos si no existe
DO
$$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'hermedb') THEN
      CREATE DATABASE "InterOp";
   END IF;
END
$$;

CREATE TABLE IF NOT EXISTS patients (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    cui VARCHAR(30) UNIQUE NOT NULL,
    birth_date DATE NOT NULL,
    address TEXT,
    phone VARCHAR(20)
);