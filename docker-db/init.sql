-- Crear base de datos si no existe
DO
$$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'hermedb') THEN
      CREATE DATABASE "InterOp";
   END IF;
END
$$;

-- Tabla de pacientes con estructura mixta: campos clave + JSONB extendido
CREATE TABLE IF NOT EXISTS pacientes (
    id SERIAL PRIMARY KEY,
    cui VARCHAR(30) UNIQUE NOT NULL,
    id_fhir TEXT UNIQUE,
    nombres TEXT,
    apellidos TEXT,
    fecha_nacimiento DATE,
    genero TEXT,
    datos_paciente JSONB, -- Datos extendidos tipo FHIR
    fecha_creacion TIMESTAMP DEFAULT now()
);

CREATE TABLE unidad_salud (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL, -- ej. USALUD001
    nombre TEXT NOT NULL,
    establecimiento_envia VARCHAR(100) NOT NULL, -- MSH-4
    sistema_envia VARCHAR(100), -- MSH-3 (opcional)
    configuracion JSONB NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS fuentes_hl7 (
    id SERIAL PRIMARY KEY,
    sistema_envia TEXT,              -- SISTEMA
    establecimiento_envia TEXT,      -- ORIGEN
    sistema_recibe TEXT,             -- DESTINO
    establecimiento_recibe TEXT,     -- Opcional
    version TEXT DEFAULT '2.3',      -- versión HL7
    tipo_mensaje TEXT,               -- TIPO_MENSAJE
    configuracion_personalizada JSONB, -- Parámetros específicos
    fecha_creacion TIMESTAMP DEFAULT now()
);