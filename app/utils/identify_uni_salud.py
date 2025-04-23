def identify_hospital(hl7_message: str) -> dict:
    msh_segment = next(seg for seg in hl7_message.split("\n") if seg.startswith("MSH"))
    fields = msh_segment.split("|")
    sending_facility = fields[4]  # MSH-4
    sending_app = fields[3]       # MSH-3

    # Buscar en la base de datos el hospital correspondiente
    hospital = db.query(Hospital).filter_by(sending_facility=sending_facility).first()

    if not hospital:
        raise ValueError("Hospital no registrado en el sistema.")

    return hospital.config