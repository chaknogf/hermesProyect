CREATE Table organizaciones (
    id SERIAL PRIMARY KEY,
    unidad INTEGER NOT NULL UNIQUE,
    departamento VARCHAR(30) NOT NULL,
    depencia VARCHAR(50) NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    estado BOOLEAN NOT NULL
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);