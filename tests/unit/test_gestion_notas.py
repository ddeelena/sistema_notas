# tests/unit/test_gestion_notas_service.py
import pytest
from sistema_notas.services.gestion_notas_service import GestionNotasService
from sistema_notas.exceptions.nota_duplicada_error import (
    NotaFueraDeRangoError,
    NotaDuplicadaError,
)


@pytest.fixture
def service():
    return GestionNotasService()


# ── REQ 1: Rango de notas ──────────────────────────────────────────────────

# TC-01: borde inferior 0.0 debe aceptarse
def test_registrar_nota_en_borde_inferior(service):
    service.registrar_nota(
        estudiante_id=1001, materia_id="MAT-01", semestre="2026-1", nota=0.0
    )
    notas = service.obtener_notas(estudiante_id=1001)
    assert notas[0].nota == 0.0


# TC-02: borde superior 5.0 debe aceptarse
def test_registrar_nota_en_borde_superior(service):
    service.registrar_nota(
        estudiante_id=1001, materia_id="MAT-01", semestre="2026-1", nota=5.0
    )
    notas = service.obtener_notas(estudiante_id=1001)
    assert notas[0].nota == 5.0


# TC-03: nota 5.1 debe lanzar NotaFueraDeRangoError
def test_registrar_nota_sobre_limite_superior_lanza_error(service):
    with pytest.raises(NotaFueraDeRangoError):
        service.registrar_nota(
            estudiante_id=1001, materia_id="MAT-01", semestre="2026-1", nota=5.1
        )


# Partición inválida: -0.5 debe lanzar NotaFueraDeRangoError
def test_registrar_nota_bajo_limite_inferior_lanza_error(service):
    with pytest.raises(NotaFueraDeRangoError):
        service.registrar_nota(
            estudiante_id=1001, materia_id="MAT-01", semestre="2026-1", nota=-0.5
        )


# Partición válida: 4.5 debe guardarse
def test_registrar_nota_valida_se_almacena(service):
    service.registrar_nota(
        estudiante_id=1001, materia_id="MAT-01", semestre="2026-1", nota=4.5
    )
    notas = service.obtener_notas(estudiante_id=1001)
    assert any(n.nota == 4.5 for n in notas)


# Partición inválida: 5.4 debe lanzar error
def test_registrar_nota_invalida_54_lanza_error(service):
    with pytest.raises(NotaFueraDeRangoError):
        service.registrar_nota(
            estudiante_id=1001, materia_id="MAT-01", semestre="2026-1", nota=5.4
        )

# ── REQ 2: Aprobación ─────────────────────────────────────────────────────

# TC-04: 2.9 -> Reprobada (borde más alto para reprobar)
def test_nota_29_resulta_en_reprobada(service):
    service.registrar_nota(1001, "MAT-01", "2026-1", 2.9)
    estado = service.obtener_estado(1001, "MAT-01", "2026-1")
    assert estado == "Reprobada"


# TC-05: 3.0 -> Aprobada (borde mínimo para aprobar)
def test_nota_30_resulta_en_aprobada(service):
    service.registrar_nota(1001, "MAT-01", "2026-1", 3.0)
    estado = service.obtener_estado(1001, "MAT-01", "2026-1")
    assert estado == "Aprobada"


# TC-06: 4.5 -> Aprobada (partición válida positiva)
def test_nota_45_resulta_en_aprobada(service):
    service.registrar_nota(1001, "MAT-01", "2026-1", 4.5)
    estado = service.obtener_estado(1001, "MAT-01", "2026-1")
    assert estado == "Aprobada"

# ── REQ 3: Promedio ───────────────────────────────────────────────────────

# TC-07: sin notas -> promedio 0.0 (sin división por cero)
def test_promedio_sin_notas_retorna_cero(service):
    promedio = service.obtener_promedio(estudiante_id=1001)
    assert promedio == 0.0


# TC-08: una sola nota -> promedio igual a la nota
def test_promedio_con_una_nota(service):
    service.registrar_nota(1001, "MAT-01", "2026-1", 4.0)
    promedio = service.obtener_promedio(estudiante_id=1001)
    assert promedio == 4.0


# TC-09: dos notas -> (3.5 + 4.2) / 2 = 3.85
def test_promedio_con_multiples_notas_calcula_correctamente(service):
    service.registrar_nota(1001, "MAT-01", "2026-1", 3.5)
    service.registrar_nota(1001, "MAT-02", "2026-1", 4.2)
    promedio = service.obtener_promedio(estudiante_id=1001)
    assert promedio == pytest.approx(3.85, rel=1e-3)

# ── REQ 4: Duplicados ─────────────────────────────────────────────────────

# TC-10: dos materias distintas, mismo semestre -> ambas se guardan
def test_dos_materias_distintas_mismo_semestre_se_guardan(service):
    service.registrar_nota(1001, "MAT-01", "2026-1", 4.0)
    service.registrar_nota(1001, "MAT-02", "2026-1", 3.5)
    notas = service.obtener_notas(estudiante_id=1001)
    assert len(notas) == 2


# TC-11: misma materia, semestres distintos -> ambas se guardan (histórico)
def test_misma_materia_semestres_distintos_se_guardan(service):
    service.registrar_nota(1001, "MAT-01", "2026-1", 2.5)
    service.registrar_nota(1001, "MAT-01", "2026-2", 4.0)
    notas = service.obtener_notas(estudiante_id=1001)
    assert len(notas) == 2


# TC-12: misma materia, mismo semestre -> lanza NotaDuplicadaError
def test_misma_materia_mismo_semestre_lanza_error_duplicado(service):
    service.registrar_nota(1001, "MAT-01", "2026-1", 3.5)
    with pytest.raises(NotaDuplicadaError):
        service.registrar_nota(1001, "MAT-01", "2026-1", 4.2)