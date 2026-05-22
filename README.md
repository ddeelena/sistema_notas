**1.1 — Particiones de equivalencia**


nombre Partición | rango | valor prueba | resultado 
nota aceptada | 0.0 - 5.0 | 4.5 | valido - se acepta el valor
nota no aceptada | 0.0 - 5.0 | 5.4 | invalido - se rechaza el valor
limite inferior | 0.0 | 0.0 | valido - se acepta el valor
por debajo del limite inferior | 0.0 | -0.5 | invalido - se recahza el valor
limite superior | 5.0 | 5.0 | valido - se acepta el valor
supera el limite | 5.0 | 5.5 | invalido - se rechaza el valor 


**1.2 — Análisis de valores límite**


Límite Analizado | Valor de Prueba | Posición respecto al Límite | Estado del Rango | Resultado Esperado

Borde inferior (0.0) | -0.1 | Justo antes | Fuera | Falla: Error de validación
Borde inferior (0.0|) | 0.0 | Exacto | Dentro | Exitoso: registra la nota
Borde inferior (0.0) | 0.1 | Justo déspues | Dentro | Exitoso: registra la nota

Aprobación borde inferior (3.0) | 2.9| Justo antes | Dentro | Exitoso:registra la nota pero reprueba
Aprobación borde inferior (3.0|) | 3.0 | Exacto | Dentro | Exitoso: registra la nota y aprueba
Aprobación borde inferior (3.0) | 3.1 | Justo déspues | Dentro | Exitoso: registra la nota y aprueba

Borde superior (5.0) | 4.9 | Justo antes | Dentro | Exitoso: registra la nota y aprueba
Borde superior (5.0|) | 5.0 | Exacto | Dentro | Exitoso: registra la nota y aprueba
Borde superior (5.0) | 5.1 | Justo déspues | Fuera | Falla: Error de validación

**1.3 — Preguntas al Product Owner**


Pregunta 1:

¿Si un estudiante reprueba una materia en el Semestre A y la matricula de nuevo en el Semestre B, ¿el sistema debe permitir registrar la nueva nota manteniendo el histórico, o la segunda nota sobrescribe/reemplaza a la primera en el historial académico?

Justificación:

Cambia totalmente la configuración de las precondiciones y los datos de prueba. Si el sistema mantiene el histórico, el caso de prueba para el cálculo del promedio (Req 3) debe incluir ambas notas en semestres diferentes para validar la fórmula. Si la sobrescribe, el caso de prueba del promedio debe verificar que la nota antigua ya no sume ni divida, y se necesitaría un test adicional de persistencia de datos.


Pregunta 2 

si un profesor se equivoca digitando un 2.5 en vez de un 4.5 y le da guardar, ¿el sistema le va a permitir corregir su error o la nota queda bloqueada para siempre por la restricción?"

Justificación

Si el sistema permite corregir o editar una nota ya guardada, tengo que diseñar casos de prueba específicos para el flujo de "Edición" (asegurándome de que el promedio se vuelva a calcular bien y que el estado cambie de Reprobado a Aprobado). Pero si el sistema no permite ediciones y la nota queda fija, mi diseño de pruebas debe enfocarse en verificar que el sistema lance un bloqueo estricto y tendríamos que probar un flujo alterno (como un proceso de anulación o una solicitud de cambio con un coordinador).

