-- Crear base de datos si no existe
DO
$$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'hermedb') THEN
      CREATE DATABASE "InterOp";
   END IF;
END
$$;
-- ESTANDAR HL7
-- Tabla de pacientes con estructura mixta: campos clave + JSONB extendido
CREATE TABLE IF NOT EXISTS patients (
    id SERIAL PRIMARY KEY,
    identifier TEXT UNIQUE NOT NULL,       -- FHIR: identifier[0].value (por ejemplo, el CUI)
    fhir_id TEXT UNIQUE,                   -- FHIR: id (del recurso FHIR)
    given TEXT,                            -- FHIR: name.given[0] (nombres)
    family TEXT,                           -- FHIR: name.family (apellidos)
    birth_date DATE,                       -- FHIR: birthDate
    gender TEXT,                           -- FHIR: gender (male | female | other | unknown)
    address JSONB,                         -- FHIR: address[] (direcciones del paciente)
    telecom JSONB,                         -- FHIR: telecom[] (teléfonos, correos, etc.)
    managing_organization TEXT,            -- FHIR: managingOrganization.reference
    extension JSONB,                       -- FHIR: extension[] (datos extendidos)
    meta JSONB,                            -- FHIR: meta (versionado, última modificación)
    created_at TIMESTAMP DEFAULT now()     -- Fecha de creación del registro
);

CREATE TABLE health_unit (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,              -- Código único de la unidad de salud (ej. USALUD001)
    name TEXT NOT NULL,                            -- Nombre de la unidad médica
    sending_facility VARCHAR(100) NOT NULL,        -- MSH-4: Establecimiento emisor
    sending_application VARCHAR(100),              -- MSH-3: Aplicación emisora (opcional)
    config JSONB NOT NULL,                         -- Configuración técnica específica en formato JSON
    is_active BOOLEAN DEFAULT TRUE                 -- Estado de operación (activo/inactivo)
);

CREATE TABLE IF NOT EXISTS hl7_sources (
    id SERIAL PRIMARY KEY,
    sending_application TEXT,                      -- MSH-3: Sistema que envía el mensaje HL7
    sending_facility TEXT,                         -- MSH-4: Establecimiento origen del mensaje
    receiving_application TEXT,                    -- MSH-5: Sistema que recibe el mensaje
    receiving_facility TEXT,                       -- MSH-6: Establecimiento receptor del mensaje
    version TEXT DEFAULT '2.3',                    -- Versión HL7 utilizada (por defecto 2.3)
    message_type TEXT,                             -- MSH-9: Tipo de mensaje HL7 (ej. ADT^A01)
    custom_config JSONB,                           -- Configuración personalizada adicional
    created_at TIMESTAMP DEFAULT now()             -- Fecha de creación del registro
);

-- ESTANDAR ESPAÑOL

-- Tabla de pacientes con estructura mixta: campos clave + JSONB extendido
CREATE TABLE IF NOT EXISTS pacientes (
    id SERIAL PRIMARY KEY,
    identificador TEXT UNIQUE NOT NULL,         -- FHIR: identifier[0].value
    id_fhir TEXT UNIQUE,                        -- FHIR: id
    nombres TEXT,                               -- FHIR: name.given[0]
    apellidos TEXT,                             -- FHIR: name.family
    fecha_nacimiento DATE,                      -- FHIR: birthDate
    genero TEXT,                                -- FHIR: gender
    direccion JSONB,                            -- FHIR: address[]
    contacto JSONB,                             -- FHIR: telecom[]
    organizacion_gestora TEXT,                  -- FHIR: managingOrganization.reference
    extensiones JSONB,                          -- FHIR: extension[]
    metadatos JSONB,                            -- FHIR: meta
    fecha_creacion TIMESTAMP DEFAULT now()
);

CREATE TABLE unidad_salud (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,              -- Código único de la unidad de salud (ej. USALUD001)
    nombre TEXT NOT NULL,                            -- Nombre de la unidad médica
    establecimiento_emisor VARCHAR(100) NOT NULL,    -- MSH-4: Establecimiento que envía el mensaje
    aplicacion_emisora VARCHAR(100),                 -- MSH-3: Aplicación emisora (opcional)
    configuracion JSONB NOT NULL,                    -- Configuración técnica específica en formato JSON
    esta_activa BOOLEAN DEFAULT TRUE                 -- Estado de operación (activo/inactivo)
);

CREATE TABLE IF NOT EXISTS fuentes_hl7 (
    id SERIAL PRIMARY KEY,
    aplicacion_emisora TEXT,                         -- MSH-3: Sistema que envía el mensaje HL7
    establecimiento_emisor TEXT,                     -- MSH-4: Establecimiento origen del mensaje
    aplicacion_receptora TEXT,                       -- MSH-5: Sistema que recibe el mensaje
    establecimiento_receptor TEXT,                   -- MSH-6: Establecimiento receptor del mensaje
    version TEXT DEFAULT '2.3',                      -- Versión HL7 utilizada (por defecto 2.3)
    tipo_mensaje TEXT,                               -- MSH-9: Tipo de mensaje HL7 (ej. ADT^A01)
    configuracion_personalizada JSONB,               -- Configuración personalizada adicional
    fecha_creacion TIMESTAMP DEFAULT now()           -- Fecha de creación del registro
);

-- minimo de datos para crear un paciente
INSERT INTO pacientes (identificador, nombres, apellidos, fecha_nacimiento, genero) VALUES ('123456', 'Juan', 'Pérez', '1990-01-01', 'male');