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

**PARTE 2 — Diseño formal de casos de prueba **

Nota de diseño: Para mantener la consistencia de las pruebas en un entorno aislado, se asume la existencia de los datos maestros: Estudiante: Juan Pérez (ID: 1001), Materias: Cálculo I (ID: MAT-01) y Física I (ID: MAT-02), Semestres: 2026-1 y 2026-2.

IDRequerimiento | Descripción | PrecondiciónDatos de entrada | PasosResultado esperado 

TipoTC-01 |
Req 1: Rango de notas | Registrar nota válida en el extremo inferior del rango. |
El estudiante Juan Pérez está matriculado en Cálculo I en el semestre 2026-1. No hay notas previas. |
Estudiante: 1001Materia: MAT-01Semestre: 2026-1 Nota: 0.0 |
1. Ingresar al módulo de registro.
2. Seleccionar estudiante, materia y semestre.
3. Digitar la nota.
4. Guardar. |
El sistema almacena la nota exitosamente. Muestra mensaje de confirmación. | Borde

TC-02 |
Req 1: Rango de notas | Registrar nota válida en el extremo superior del rango. | 
El estudiante Juan Pérez está matriculado en Cálculo I en el semestre 2026-1. No hay notas previas. |
Estudiante: 1001Materia: MAT-01Semestre: 2026-1Nota: 5.0 |
1. Ingresar al módulo de registro.
2. Seleccionar estudiante, materia y semestre.
3. Digitar la nota.
4. Guardar. |
El sistema almacena la nota exitosamente. Muestra mensaje de confirmación. | Borde

TC-03 | 
Req 1: Rango de notas | Intentar registrar una nota que excede el límite máximo permitido. |
El estudiante Juan Pérez está matriculado en Cálculo I en el semestre 2026-1. No hay notas previas.|Estudiante: 1001Materia: MAT-01Semestre: 2026-1Nota: 5.1 |
1. Ingresar al módulo de registro.
2. Seleccionar estudiante, materia y semestre.
3. Digitar la nota.
4. Intentar guardar. |
El sistema bloquea el registro y despliega el mensaje de error: "La nota debe estar entre 0.0 y 5.0". | Negativo

TC-04 | 
Req 2: Aprobación | Validar reprobación con la nota más alta posible para perder. | 
El estudiante Juan Pérez está matriculado en Cálculo I en el semestre 2026-1. No hay notas previas.|Estudiante: 1001Materia: MAT-01Semestre: 2026-1Nota: 2.9 |
1. Registrar la nota del estudiante con los datos de entrada.
2. Consultar el estado académico de la materia para ese estudiante.| 
La nota se guarda con éxito. El estado asignado de la materia es: Reprobada. | Borde

TC-05 | 
Req 2: Aprobación | Validar aprobación con la nota mínima requerida. |
El estudiante Juan Pérez está matriculado en Cálculo I en el semestre 2026-1. No hay notas previas.|Estudiante: 1001Materia: MAT-01Semestre: 2026-1Nota: 3.0 |
1. Registrar la nota del estudiante con los datos de entrada. 
2. Consultar el estado académico de la materia para ese estudiante.La nota se guarda con éxito. | El estado asignado de la materia es: Aprobada. | Borde 

TC-06 | 
Req 2: Aprobación | Validar aprobación con una nota intermedia alta dentro de la partición válida.|El estudiante Juan Pérez está matriculado en Cálculo I en el semestre 2026-1. No hay notas previas.|Estudiante: 1001Materia: MAT-01Semestre: 2026-1Nota: 4.5 | 
1. Registrar la nota del estudiante con los datos de entrada.
2. Consultar el estado académico de la materia para ese estudiante.La nota se guarda con éxito. El estado asignado de la materia es: Aprobada.| Positivo 

TC-07 |
Req 3: Promedio | Calcular el promedio para un estudiante que aún no posee registros. |
El estudiante Juan Pérez existe en el sistema pero no se le ha registrado ninguna nota históricamente. | 
Estudiante: 1001 |
1. Ingresar al perfil o reporte de calificaciones del estudiante.
2. Visualizar el campo de promedio acumulado. |
El sistema responde de manera controlada mostrando un promedio de 0.0 (evitando errores de división por cero). | Negativo 

TC-08 | 
Req 3: Promedio | Calcular el promedio simple con una única nota registrada. | 
El estudiante Juan Pérez tiene una sola nota registrada en su historial. | 
Estudiante: 1001 (Con una nota de 4.0 en Cálculo I) |
1. Ingresar al perfil o reporte de calificaciones del estudiante.
2. Visualizar el campo de promedio acumulado. | 
El sistema calcula el promedio de manera exacta, mostrando 4.0. | Positivo

TC-09 | 
Req 3: Promedio | Calcular el promedio compuesto con múltiples notas que generan decimales. | 
El estudiante Juan Pérez tiene dos notas registradas en diferentes materias. | 
Estudiante: 1001 (Notas registradas: 3.5 en Cálculo I y 4.2 en Física I) | 
1. Ingresar al perfil o reporte de calificaciones del estudiante.
2. Visualizar el campo de promedio acumulado. | 
El sistema realiza la operación (3.5 + 4.2) / 2 y muestra el promedio exacto de 3.85. | Positivo

TC-10 | 
Req 4: Duplicados| Registrar dos materias distintas dentro del mismo semestre académico. | 
El estudiante Juan Pérez está matriculado en Cálculo I y Física I en el semestre 2026-1. No tiene notas previas. | 
Registro 1: Materia: MAT-01, Nota: 4.0Registro 2: Materia: MAT-02, Nota: 3.5(Ambos para Estudiante 1001, Semestre 2026-1) | 
1. Completar el proceso de registro para la materia MAT-01.
2. Iniciar un nuevo proceso de registro para la materia MAT-02 en el mismo semestre. |
Ambos registros se almacenan de manera exitosa en el sistema sin generar conflictos. | Positivo

TC-11 | 
Req 4: Duplicados | Registrar la misma materia en dos semestres consecutivos diferentes. | 
El estudiante Juan Pérez cursó la materia en 2026-1 (y ya tiene nota) y volvió a matricularla en 2026-2. | 
Registro 1 (Previo): Semestre: 2026-1, Nota: 2.5 Registro 2 (Nuevo): Semestre: 2026-2, Nota: 4.0(Ambos para Estudiante 1001, Materia MAT-01) | 
1. Validar que exista el registro del semestre 2026-1.
2. Proceder a registrar la nueva nota utilizando el semestre 2026-2. | 
El segundo registro se procesa con éxito, permitiendo el histórico transaccional de la materia. |Positivo

TC-12 |
Req 4: Duplicados | Intentar registrar una segunda nota para la misma materia y el mismo semestre. |El estudiante Juan Pérez ya cuenta con una nota guardada de 3.5 para Cálculo I en el semestre 2026-1. | 
Estudiante: 1001Materia: MAT-01Semestre: 2026-1Nota: 4.2 | 
1. Ingresar al módulo de registro.
2. Digitar los datos de entrada que duplican la combinación de llave existente.
3. Intentar guardar. | 
El sistema rechaza la transacción y lanza el error en pantalla: "El estudiante ya tiene una nota registrada para esta materia en el semestre seleccionado". | Negativo


REFLEXIÓN

Primero: ¿qué diferencia notaste entre diseñar los casos de prueba en la tabla antes de escribir código versus simplemente ponerte a programar directamente?

La diferencia es clara, como ya tenia los casos de pruebas listos, solamente era "hacer la traduccion" mas no tenía que detenerme a pensar en que pruebas tenía que hacer con que dato si o con que dato y démas


Segundo: ¿qué fue lo más difícil de seguir el ciclo TDD y en qué momento sentiste la tentación de saltarte algún paso?

En el ciclo de TDD creo que lo más difícil es la refactorización porque en algunos casos no es tan visible que mejorar si en la fase green se penso en hacerlo bien, ya que aunque se supone que es hacerlo solo para que pase a veces directamente yo hacía la función completa y como debería quedar refactorizada y  luego me tenía que devolver a hacerla un poco más sencilla o quitarle algún complemento. 

En el último requisito no es que quisiera saltarme pasos solo apenas realice el test ya habian pasado por las implementaciones de las demás funcionalidades, mientras que en el requisito 3 en el promedio no sabía que más poner entonces pensé en no hacer refactor. 



