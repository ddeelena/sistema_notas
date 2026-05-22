class NotaDuplicadaError(Exception):
    """Ya existe una nota para esta materia en este semestre."""
    pass

class NotaFueraDeRangoError(Exception):
    """La nota está fuera del rango permitido (0.0 - 5.0)."""
    pass