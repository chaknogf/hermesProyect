# hermesProyect

prototipo api interoperatibilidad LH7-FHIR

## 🩺 API FHIR Interop – Proyecto FastAPI

Esta API está diseñada para facilitar la interoperabilidad médica mediante el estándar HL7 FHIR. Utiliza FastAPI como framework principal.

---

## ⚙️ Requisitos

- Python 3.10+
- pip
- Git (opcional)
- PostgreSQL (si se usa base de datos más adelante)

---

## 🐍 Crear y activar entorno virtual

### 🔧 En Windows (PowerShell o CMD)

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 🔧 En Linux (bash/zsh)

```python3 -m venv venv
source venv/bin/activate
```

## 📦 Instalar dependencias

```pip install -r requirements.txt
```

## 🚀 Iniciar servidor de desarrollo

```uvicorn main:app --reload
```

 • Documentación interactiva: <http://localhost:8000/docs>
 • OpenAPI JSON: <http://localhost:8000/openapi.json>
