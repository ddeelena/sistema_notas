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