# src/sistema_notas/repositories/gestion_notas_repository.py

from sistema_notas.models.nota import Nota
from sistema_notas.database.database import get_connection


class GestionNotasRepository:

    def guardar(self, nota: Nota) -> None:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO notas (
                estudiante_id,
                materia_id,
                semestre,
                nota
            )
            VALUES (%s, %s, %s, %s)
        """, (
            nota.estudiante_id,
            nota.materia_id,
            nota.semestre,
            nota.nota
        ))

        conn.commit()
        cursor.close()
        conn.close()

    def buscar_por_estudiante(self, estudiante_id: int) -> list[Nota]:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT estudiante_id, materia_id, semestre, nota
            FROM notas
            WHERE estudiante_id = %s
        """, (estudiante_id,))

        filas = cursor.fetchall()

        cursor.close()
        conn.close()

        return [
            Nota(
                estudiante_id=fila[0],
                materia_id=fila[1],
                semestre=fila[2],
                nota=float(fila[3])
            )
            for fila in filas
        ]

    def existe(
        self,
        estudiante_id: int,
        materia_id: str,
        semestre: str
    ) -> bool:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM notas
            WHERE estudiante_id = %s
            AND materia_id = %s
            AND semestre = %s
        """, (
            estudiante_id,
            materia_id,
            semestre
        ))

        existe = cursor.fetchone()[0] > 0

        cursor.close()
        conn.close()

        return existe

    def buscar_nota(
        self,
        estudiante_id: int,
        materia_id: str,
        semestre: str
    ) -> Nota | None:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT estudiante_id, materia_id, semestre, nota
            FROM notas
            WHERE estudiante_id = %s
            AND materia_id = %s
            AND semestre = %s
        """, (
            estudiante_id,
            materia_id,
            semestre
        ))

        fila = cursor.fetchone()

        cursor.close()
        conn.close()

        if fila:
            return Nota(
                estudiante_id=fila[0],
                materia_id=fila[1],
                semestre=fila[2],
                nota=float(fila[3])
            )

        return None

    def limpiar_tabla(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("TRUNCATE TABLE notas")

        conn.commit()
        cursor.close()
        conn.close()

    def listar_todas(self) -> list[Nota]:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT estudiante_id, materia_id, semestre, nota
            FROM notas
            ORDER BY estudiante_id
        """)

        filas = cursor.fetchall()

        cursor.close()
        conn.close()

        return [
            Nota(
                estudiante_id=fila[0],
                materia_id=fila[1],
                semestre=fila[2],
                nota=float(fila[3])
            )
            for fila in filas
        ]
    
    def eliminar( self, estudiante_id: int, materia_id: str, semestre: str) -> bool:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM notas
            WHERE estudiante_id = %s
            AND materia_id = %s
            AND semestre = %s
        """, (
            estudiante_id,
            materia_id,
            semestre
        ))

        eliminado = cursor.rowcount > 0

        conn.commit()
        cursor.close()
        conn.close()

        return eliminado