CREATE TABLE pacientes (
    id SERIAL PRIMARY KEY,
     -- 🔐 Identificadores múltiples
    identificadores JSONB NOT NULL, -- Ej: [{ "tipo": "DPI", "valor": "1234567890101" }, { "tipo": "expediente", "valor": "20250001" }]
    -- 🧍‍♂️ Identificación personal
    primer_nombre VARCHAR(50),
    segundo_nombre VARCHAR(50),
    primer_apellido VARCHAR(50),
    segundo_apellido VARCHAR(50),
    sexo VARCHAR(2),
    fecha_nacimiento DATE,
    -- ☎️ Contacto
    contacto JSONB,         -- { "telefono": "...", "email": "...", "direccion": "..." }
    -- 👪 Referencias
    referencias JSONB,      -- [{ "nombre": "...", "parentesco": "...", "telefono": "..." }]
    -- 🌍 Otros datos del paciente
    datos_extra JSONB,      -- { "nacionalidad": "...", "ocupacion": "...", "idiomas": [...] }
    -- ⚙️ Metadatos del sistema
    estado VARCHAR(2) DEFAULT 'A',         -- 'A'=Activo, 'I'=Inactivo, 'F'=Fallecido
    metadatos JSONB,
    resumen_clinico JSONB,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);