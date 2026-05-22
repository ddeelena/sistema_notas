from sistema_notas.models.nota import Nota


class GestionNotasRepository:
    def __init__(self):
        self._store: list[Nota] = []

    def guardar(self, nota: Nota) -> None:
        self._store.append(nota)

    def buscar_por_estudiante(self, estudiante_id: int) -> list[Nota]:
        return [n for n in self._store if n.estudiante_id == estudiante_id]

    def existe(self, estudiante_id: int, materia_id: str, semestre: str) -> bool:
        return any(
            n.estudiante_id == estudiante_id
            and n.materia_id == materia_id
            and n.semestre == semestre
            for n in self._store
        )