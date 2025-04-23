from fhir.resources.patient import Patient
from fhir.resources.humanname import HumanName
from fhir.resources.identifier import Identifier

def hl7_to_fhir_patient(hl7_message: str) -> Patient:
    """
    Convierte un mensaje HL7v2 en un recurso FHIR Patient (simplificado).
    """
    lines = hl7_message.strip().split("\n")
    segments = {line.split("|")[0]: line.split("|") for line in lines}

    pid = segments.get("PID", [])
    if not pid:
        raise ValueError("No se encontró el segmento PID en el mensaje HL7")

    # Extraer datos básicos
    patient_id = pid[3] if len(pid) > 3 else "desconocido"
    full_name = pid[5].split("^") if len(pid) > 5 else ["", ""]

    fhir_patient = Patient.construct(
        id=patient_id,
        identifier=[
            Identifier.construct(system="urn:hl7-org:v2", value=patient_id)
        ],
        name=[
            HumanName.construct(
                family=full_name[0],
                given=[full_name[1]]
            )
        ]
    )

    return fhir_patient