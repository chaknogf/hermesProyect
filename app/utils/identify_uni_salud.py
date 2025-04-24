def identificar_unidad_salud(hl7_message: str, db: Session) -> dict:
    msh_segment = next(seg for seg in hl7_message.split("\n") if seg.startswith("MSH"))
    campos = msh_segment.split("|")
    sending_facility = campos[4]  # MSH-4

    unidad = db.query(UnidadSalud).filter_by(sending_facility=sending_facility).first()

    if not unidad:
        raise ValueError(f"Unidad de salud '{sending_facility}' no registrada.")

    return unidad.config