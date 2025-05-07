CREATE TABLE consultas (
    id SERIAL PRIMARY KEY,
    organizacion_id INTEGER REFERENCES unidades_salud(id) NOT NULL,
    paciente_id INTEGER REFERENCES pacientes(id) NOT NULL,
    tipo_consulta INTEGER,
    especialidad INTEGER,
    servicio VARCHAR(50),
    documento VARCHAR(20),
    fecha_consulta DATE,
    hora_consulta TIME,
    ciclo JSONB, -- { 
              --   "activo": "2025-05-06T10:00:00", 
              --   "egreso": "2025-05-06T15:00:00", 
              --   "archivado": "2025-05-07T08:00:00", 
              --   "prestamo": "2025-05-07T10:30:00", 
              --   "reactivado": "2025-05-08T09:00:00"
              -- }

    indicadores JSONB, -- {"prenatal": 4, "lactancia": true, "bomberos": true, "arma_blanca": false, ...}
    detalle_clinico JSONB, -- {"medico": "Dr. Juan", "diagnostico": "Cancer", "tratamiento": "Quimioterapia", ...}
    signos_vitales JSONB, -- {"temperatura": 36.5, "presion_arterial": "120/80", "frecuencia_cardiaca": 60, ...}
    ansigmas JSONB, -- {"sintomas": ["dolor de cabeza", "nauseas", "diarrea"], "examen_fisico": "Normal", ...}
    antecedentes JSONB, -- {"alergias": ["penicilina", "antibiotico"], "enfermedades": ["diabetes", "hipertension"], ...}
    ordenes JSONB, -- {"medicamentos": ["paracetamol", "ibuprofeno"], "examen_fisico": "Normal", ...}
    estudios JSONB, -- {"laboratorios": ["hemograma", "electrocardiograma"], "rayos_x": "Normal", ...}
    -- 🧾 Metadatos
    metadatos JSONB,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
);