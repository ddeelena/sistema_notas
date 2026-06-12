# src/sistema_notas/services/gestion_notas_service.py

from sistema_notas.models.nota import Nota
from sistema_notas.repositories.gestion_notas_repository import GestionNotasRepository
from sistema_notas.exceptions.nota_duplicada_error import (
    NotaFueraDeRangoError,
    NotaDuplicadaError,
)
from sistema_notas.exceptions.nota_no_encontrada import NotaNoEncontradaError


NOTA_MIN = 0.0
NOTA_MAX = 5.0

MENSAJE_RANGO = f"La nota debe estar entre {NOTA_MIN} y {NOTA_MAX}."
MENSAJE_DUPLICADA = (
    "El estudiante ya tiene una nota registrada para esta materia en el semestre seleccionado."
)
MENSAJE_NOTA_NO_ENCONTRADA = (
    "No se encontró una nota para esta materia en este semestre."
)


class GestionNotasService:

    def __init__(self):
        self.repository = GestionNotasRepository()

    def registrar_nota(
        self,
        estudiante_id: int,
        materia_id: str,
        semestre: str,
        nota: float
    ) -> Nota:

        self.validar_rango_nota(nota)
        self.validar_nota_duplicada(
            estudiante_id,
            materia_id,
            semestre
        )

        nueva_nota = Nota(
            estudiante_id=estudiante_id,
            materia_id=materia_id,
            semestre=semestre,
            nota=nota
        )

        self.repository.guardar(nueva_nota)

        return nueva_nota

    def obtener_notas(self, estudiante_id: int) -> list[Nota]:
        return self.repository.buscar_por_estudiante(estudiante_id)

    def validar_rango_nota(self, nota: float):
        if nota < NOTA_MIN or nota > NOTA_MAX:
            raise NotaFueraDeRangoError(MENSAJE_RANGO)

    def validar_nota_duplicada(
        self,
        estudiante_id: int,
        materia_id: str,
        semestre: str
    ):
        if self.repository.existe(
            estudiante_id,
            materia_id,
            semestre
        ):
            raise NotaDuplicadaError(MENSAJE_DUPLICADA)

    def obtener_estado(
        self,
        estudiante_id: int,
        materia_id: str,
        semestre: str
    ) -> str:

        nota = self.repository.buscar_nota(
            estudiante_id,
            materia_id,
            semestre
        )

        if nota is None:
            raise NotaNoEncontradaError(
                MENSAJE_NOTA_NO_ENCONTRADA
            )

        return (
            "Aprobada"
            if nota.nota >= 3.0
            else "Reprobada"
        )

    def obtener_promedio(self, estudiante_id: int) -> float:
        notas = self.repository.buscar_por_estudiante(estudiante_id)

        if not notas:
            return 0.0

        total = sum(float(n.nota) for n in notas)

        return round(total / len(notas), 2)
    
    def listar_notas(self) -> list[Nota]:
        return self.repository.listar_todas()
    
    def eliminar_nota( self, estudiante_id: int, materia_id: str, semestre: str) -> None:

        eliminado = self.repository.eliminar(
            estudiante_id,
            materia_id,
            semestre
        )

        if not eliminado:
            raise NotaNoEncontradaError(
                MENSAJE_NOTA_NO_ENCONTRADA
            )