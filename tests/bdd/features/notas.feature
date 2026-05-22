Feature: Gestión de calificaciones académicas
  Como docente de la universidad,
  quiero registrar y consultar las notas de mis estudiantes,
  para que el sistema determine su estado académico,
  calcule su promedio y evite registros duplicados.

  Background:
    Given el estudiante con ID 1001 existe en el sistema
    And la materia con ID MAT-01 existe en el sistema
    And la materia con ID MAT-02 existe en el sistema

  # ── Req 2: Aprobación ────────────────────────────────────────────────────

  @smoke @critical
  Scenario: El estudiante reprueba con la nota más alta posible para perder
    When el docente registra la nota 2.9 para el estudiante 1001 en MAT-01 semestre 2026-1
    Then el estado de MAT-01 en 2026-1 para el estudiante 1001 es "Reprobada"

  @smoke @critical
  Scenario: El estudiante aprueba con la nota mínima requerida
    When el docente registra la nota 3.0 para el estudiante 1001 en MAT-01 semestre 2026-1
    Then el estado de MAT-01 en 2026-1 para el estudiante 1001 es "Aprobada"

  @regression
  Scenario Outline: El estado varía según el umbral de aprobación
    When el docente registra la nota <nota> para el estudiante 1001 en MAT-01 semestre 2026-1
    Then el estado de MAT-01 en 2026-1 para el estudiante 1001 es "<estado>"

    Examples:
      | nota | estado    |
      | 0.0  | Reprobada |
      | 2.9  | Reprobada |
      | 3.0  | Aprobada  |
      | 4.5  | Aprobada  |
      | 5.0  | Aprobada  |

  # ── Req 3: Promedio ───────────────────────────────────────────────────────

  @smoke
  Scenario: El sistema calcula el promedio con dos materias registradas
    When el docente registra la nota 3.5 para el estudiante 1001 en MAT-01 semestre 2026-1
    And el docente registra la nota 4.2 para el estudiante 1001 en MAT-02 semestre 2026-1
    Then el promedio del estudiante 1001 es 3.85

  @regression
  Scenario: El promedio de un estudiante sin notas es cero
    When el docente consulta el promedio del estudiante 1001
    Then el promedio del estudiante 1001 es 0.0

  # ── Req 4: Duplicados ─────────────────────────────────────────────────────

  @critical
  Scenario: El sistema rechaza registrar la misma materia dos veces en el mismo semestre
    Given el docente ya registró la nota 3.5 para el estudiante 1001 en MAT-01 semestre 2026-1
    When el docente intenta registrar la nota 4.2 para el estudiante 1001 en MAT-01 semestre 2026-1
    Then el sistema rechaza el registro con el mensaje "El estudiante ya tiene una nota registrada para esta materia en el semestre seleccionado."

  @regression
  Scenario: El sistema permite registrar la misma materia en semestres diferentes
    Given el docente ya registró la nota 2.5 para el estudiante 1001 en MAT-01 semestre 2026-1
    When el docente registra la nota 4.0 para el estudiante 1001 en MAT-01 semestre 2026-2
    Then el estudiante 1001 tiene 2 notas registradas en total