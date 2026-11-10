# Tareas del Proyecto - ProyectoWebLavadoras

Roadmap de implementación organizado por fases. Se actualiza a medida que se completan tareas.

---

## ✅ Tareas Completadas

### Repositorio de Solicitud
- [x] Crear interfaz `SolicitudRepository` en `domain/repositories/`
- [x] Crear implementación `InMemorySolicitudRepository` en `infrastructure/repositories/`
- [x] Escribir pruebas del repositorio (8 pruebas, todas pasando)
- [x] Ejecutar y validar todas las pruebas (57/57 passing)

### Repositorio de Servicio
- [x] Crear interfaz `ServicioRepository` en `domain/repositories/`
- [x] Crear implementación `InMemoryServicioRepository` en `infrastructure/repositories/`
- [x] Escribir pruebas del repositorio de Servicio (6 pruebas, todas pasando)

### Casos de uso de Solicitud (Application Layer)
- [x] `CrearSolicitud` - Caso de uso para crear solicitudes (con prueba en `tests/application/test_crear_solicitud.py`)
- [x] `ListarSolicitudes` - Caso de uso para listar solicitudes, con orden cronológico
- [x] **#8** `RechazarSolicitud` - Caso de uso para rechazar solicitudes
- [x] **#13** `ConvertirSolicitudEnServicio` - Caso de uso para convertir solicitud en servicio

### Casos de uso de Servicio (Application Layer)
- [x] `MarcarServicioProximoAIniciar` - Caso de uso para avisar que el técnico está cerca, pasa un servicio de PENDIENTE a PROXIMO_A_INICIAR (con 2 pruebas en `tests/application/test_marcar_servicio_proximo_a_iniciar.py`)
- [x] **#16** `IniciarServicio` - Caso de uso para pasar un servicio de PROXIMO_A_INICIAR a EN_CURSO (con 2 pruebas en `tests/application/test_iniciar_servicio.py`)
- [x] **#17** `FinalizarServicio` - Caso de uso para pasar un servicio de EN_CURSO a FINALIZADO (con 2 pruebas en `tests/application/test_finalizar_servicio.py`)
- [x] **#15** `MostrarCitasHoy` - Caso de uso para listar servicios del día, de las 00:00 a las 23:59:59 de hoy (con 2 pruebas en `tests/application/test_mostrar_citas_hoy.py`)

### Base de datos (Fase 4)
- [x] Verificar entorno: SQL Server Express (`localhost\SQLEXPRESS`), driver `ODBC Driver 17 for SQL Server` y `pyodbc`
- [x] Crear las bases `LavadorasDB` (real) y `LavadorasTestDB` (pruebas) con las tablas `Solicitud` y `Servicio` (id con `IDENTITY`)
- [x] Guardar las cadenas de conexión en `.env` (`DB_CONNECTION_STRING` y `TEST_DB_CONNECTION_STRING`), ignorado por Git
- [x] **#9** `SqlServerSolicitudRepository` - Implementación con pyodbc, con sus 5 métodos y 6 pruebas de integración en `tests/infrastructure/test_sql_server_solicitud_repository.py`:
  - [x] `obtener_por_id`
  - [x] `guardar` con `INSERT` (asigna el id con `OUTPUT INSERTED.id`) y `UPDATE`
  - [x] `listar_por_estado` (filtra con `WHERE estado = ?`, convirtiendo el enum con `.name`)
  - [x] `listar_todas`, ordenada por `hora_solicitada`
  - [x] `eliminar`, devuelve `True`/`False` según `rowcount`
  - [x] Método auxiliar `_fila_a_solicitud` (un solo lugar para traducir fila → `Solicitud`)
- [x] **#10** `SqlServerServicioRepository` - Implementación con pyodbc, con sus 6 métodos y 7 pruebas de integración en `tests/infrastructure/test_sql_server_servicio_repository.py`:
  - [x] `obtener_por_id`
  - [x] `guardar` con `INSERT` (10 columnas, sin `id`) y `UPDATE`
  - [x] `listar_todos`, ordenada por `fecha_hora_inicio`
  - [x] `listar_por_estado`
  - [x] `listar_por_rango` (filtra por `fecha_hora_inicio` entre los dos extremos, ambos incluidos)
  - [x] `eliminar`, devuelve `True`/`False` según `rowcount`
  - [x] Método auxiliar `_fila_a_servicio` (traduce fila → `Servicio` y asigna los campos reales y calculados después de construirlo)

### Mantenimiento
- [x] Mover `test_rechazar_solicitud.py` a `tests/application/` y renombrar su test con un nombre descriptivo
- [x] Agregar `pytest.ini` en la raíz para que `pytest` encuentre los módulos del proyecto
- [x] Agregar `.gitignore` y subir el proyecto a GitHub
- [x] Renombrar `git.ignore` a `.gitignore` (con el nombre equivocado Git no ignoraba nada)
- [x] Sacar los archivos `.pyc` y `__pycache__` del repositorio
- [x] Ampliar el helper de tests `crear_solicitud` con el parámetro `hora_solicitada`
- [x] Crear el helper de tests `crear_servicio` con `problema`, `estado` y `fecha_hora_inicio`

---

## ⏳ Tareas Pendientes

### 🌐 Fase 5: API REST
- [ ] **#5** Crear API con FastAPI (endpoints que delegan a casos de uso)

### 🧹 Pendientes menores
- [ ] Escribir `README.md` (qué hace el proyecto, cómo correr `pytest`, estructura de carpetas)
- [ ] Poner descripción y topics al repositorio de GitHub (hoy es privado: hacerlo público cuando esté presentable, tras confirmar que `.env` nunca entró al historial)
- [ ] Renombrar el test `test_eliminar_borra_la_solicitud_y_devuelve_true` del repositorio de Servicio a `..._borra_el_servicio_...`
- [ ] Notificar al cliente cuando el servicio pasa a PROXIMO_A_INICIAR (efecto de infraestructura, fuera del dominio)
- [ ] Implementar la regla de negocio de agendar solo entre las 6 am y las 4 pm (hoy nada la valida)
- [ ] Renombrar el parámetro `solicitud` a `servicio` en `guardar` de `ServicioRepository` y de `InMemoryServicioRepository`
- [ ] Separar los tests de integración (necesitan SQL Server encendido) de los unitarios, para poder correrlos por separado
- [ ] Devolver las anotaciones de tipo en las firmas de los repositorios SQL

---

## ⚠️ Deuda técnica conocida

- El test de `IniciarServicio` no detecta que falte la llamada a `guardar`, porque el repositorio en memoria guarda el mismo objeto. Probar el caso de uso contra `SqlServerServicioRepository`, donde sí importará.
- `ConvertirSolicitudEnServicio` crea el servicio con `id=1` fijo. Con `IDENTITY` el id lo asigna la base, así que hay que crear el servicio con `id=None`. Verificar que esté corregido antes de la API.
- `CrearSolicitud` y `ConvertirSolicitudEnServicio` deben crear las entidades con `id=None` (los constructores lo aceptan, pero hay que revisar los casos de uso).
- `IniciarServicio`, `MarcarServicioProximoAIniciar` y `FinalizarServicio` no validan que el servicio exista: si `obtener_por_id` no encuentra nada, el siguiente paso falla con un error poco claro. Agregar la validación (y su prueba) en los tres.
- `MostrarCitasHoy` usa `date.today()` por dentro, así que sus tests dependen de la fecha del sistema. Si hiciera falta, pasar la fecha como parámetro de `ejecutar`.
- En los dos repositorios SQL, los métodos de lectura (`obtener_por_id` y los `listar_*`) usan `with` (que en `pyodbc` no cierra la conexión), mientras `guardar` y `eliminar` usan `try/finally` con `close()`. Unificar el estilo de conexión.

---

## 📊 Progreso General

```
Tareas completadas: 17/18 (94.4%)
Tareas pendientes:   1/18 (5.6%)
```

### Desglose por capa
```
Domain:          [██████████] 100% (5/5)
Infrastructure:  [██████████] 100% (4/4)
Application:     [██████████] 100% (8/8)
Presentation:    [░░░░░░░░░░]   0% (0/1)
```

---