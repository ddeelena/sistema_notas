from sistema_notas.models.nota import Nota
from sistema_notas.repositories.gestion_notas_repository import GestionNotasRepository
from sistema_notas.exceptions.nota_duplicada_error import NotaFueraDeRangoError, NotaDuplicadaError

NOTA_MIN = 0.0
NOTA_MAX = 5.0

class GestionNotasService:
    def __init__(self):
        self.repository = GestionNotasRepository()

    def registrar_nota(self, estudiante_id: int, materia_id: str, semestre: str, nota: float) -> Nota:
        # Validar rango de nota
        if nota < NOTA_MIN or nota > NOTA_MAX:
            raise NotaFueraDeRangoError(f"La nota debe estar entre {NOTA_MIN} y {NOTA_MAX}.")

        # Validar que no exista una nota para esta materia y semestre
        if self.repository.existe(estudiante_id, materia_id, semestre):
            raise NotaDuplicadaError("Ya existe una nota para esta materia en este semestre.")

        nueva_nota = Nota(estudiante_id=estudiante_id, materia_id=materia_id, semestre=semestre, nota=nota)
        self.repository.guardar(nueva_nota)

    def obtener_notas(self, estudiante_id: int) -> list[Nota]:
        return self.repository.buscar_por_estudiante(estudiante_id)