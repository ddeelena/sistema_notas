# tests/bdd/steps/test_notas_steps.py
import pytest
from pytest_bdd import given, when, then, parsers, scenarios
from sistema_notas.services.gestion_notas_service import GestionNotasService
from sistema_notas.exceptions.nota_duplicada_error import NotaDuplicadaError
from sistema_notas.database.database import get_connection

scenarios("../features/notas.feature")




@pytest.fixture
def ctx():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("TRUNCATE TABLE notas")

    conn.commit()
    cursor.close()
    conn.close()

    return {
        "service": GestionNotasService(),
        "ultimo_error": None
    }

# ── GIVEN ──────────────────────────────────────────────────────────────────

@given(parsers.parse("el estudiante con ID {estudiante_id:d} existe en el sistema"))
def estudiante_existe(ctx, estudiante_id):
    ctx["estudiante_id"] = estudiante_id


@given(parsers.parse("la materia con ID {materia_id} existe en el sistema"))
def materia_existe(ctx, materia_id):
    pass


@given(parsers.parse(
    "el docente ya registró la nota {nota:f} para el estudiante "
    "{estudiante_id:d} en {materia_id} semestre {semestre}"
))
def docente_ya_registro(ctx, nota, estudiante_id, materia_id, semestre):
    ctx["service"].registrar_nota(
        estudiante_id=estudiante_id,
        materia_id=materia_id,
        semestre=semestre,
        nota=nota,
    )


# ── WHEN ───────────────────────────────────────────────────────────────────

@when(parsers.parse(
    "el docente registra la nota {nota:f} para el estudiante "
    "{estudiante_id:d} en {materia_id} semestre {semestre}"
))
def docente_registra(ctx, nota, estudiante_id, materia_id, semestre):
    ctx["service"].registrar_nota(
        estudiante_id=estudiante_id,
        materia_id=materia_id,
        semestre=semestre,
        nota=nota,
    )


@when(parsers.parse(
    "el docente intenta registrar la nota {nota:f} para el estudiante "
    "{estudiante_id:d} en {materia_id} semestre {semestre}"
))
def docente_intenta_registrar(ctx, nota, estudiante_id, materia_id, semestre):
    try:
        ctx["service"].registrar_nota(
            estudiante_id=estudiante_id,
            materia_id=materia_id,
            semestre=semestre,
            nota=nota,
        )
    except NotaDuplicadaError as e:
        ctx["ultimo_error"] = str(e)


@when(parsers.parse("el docente consulta el promedio del estudiante {estudiante_id:d}"))
def docente_consulta_promedio(ctx, estudiante_id):
    pass


# ── THEN ───────────────────────────────────────────────────────────────────

@then(parsers.parse(
    'el estado de {materia_id} en {semestre} para el estudiante {estudiante_id:d} es "{estado}"'
))
def verificar_estado(ctx, materia_id, semestre, estudiante_id, estado):
    resultado = ctx["service"].obtener_estado(
        estudiante_id=estudiante_id,
        materia_id=materia_id,
        semestre=semestre,
    )
    assert resultado == estado


@then(parsers.parse("el promedio del estudiante {estudiante_id:d} es {esperado:f}"))
def verificar_promedio(ctx, estudiante_id, esperado):
    promedio = ctx["service"].obtener_promedio(estudiante_id=estudiante_id)
    assert abs(promedio - esperado) < 0.01


@then(parsers.parse('el sistema rechaza el registro con el mensaje "{mensaje}"'))
def verificar_rechazo(ctx, mensaje):
    assert ctx["ultimo_error"] is not None
    assert mensaje in ctx["ultimo_error"]


@then(parsers.parse("el estudiante {estudiante_id:d} tiene {cantidad:d} notas registradas en total"))
def verificar_total_notas(ctx, estudiante_id, cantidad):
    notas = ctx["service"].obtener_notas(estudiante_id=estudiante_id)
    assert len(notas) == cantidad