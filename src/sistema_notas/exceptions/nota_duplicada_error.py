class NotaDuplicadaError(Exception):
    """El estudiante ya tiene una nota registrada para esta materia en el semestre seleccionado."""
    pass

class NotaFueraDeRangoError(Exception):
    """La nota está fuera del rango permitido (0.0 - 5.0)."""
    pass