from dataclasses import dataclass


@dataclass
class Nota:
    estudiante_id: int
    materia_id: str
    semestre: str
    nota: float