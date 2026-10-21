# Tareas del Proyecto - ProyectoWebLavadoras

Roadmap de implementación organizado por fases. Se actualiza a medida que se completan tareas.

---

## ✅ Tareas Completadas

### Repositorio de Solicitud
- [x] Crear interfaz `SolicitudRepository` en `domain/repositories/`
- [x] Crear implementación `InMemorySolicitudRepository` en `infrastructure/repositories/`
- [x] Escribir pruebas del repositorio (8 pruebas, todas pasando)
- [x] Ejecutar y validar todas las pruebas (46/46 passing)

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

### Base de datos (Fase 4, avance)
- [x] Verificar entorno: SQL Server Express (`localhost\SQLEXPRESS`), driver `ODBC Driver 17 for SQL Server` y `pyodbc`
- [x] Crear las bases `LavadorasDB` (real) y `LavadorasTestDB` (pruebas) con las tablas `Solicitud` y `Servicio` (id con `IDENTITY`)
- [x] Guardar las cadenas de conexión en `.env` (`DB_CONNECTION_STRING` y `TEST_DB_CONNECTION_STRING`), ignorado por Git

### Mantenimiento
- [x] Mover `test_rechazar_solicitud.py` a `tests/application/` y renombrar su test con un nombre descriptivo
- [x] Agregar `pytest.ini` en la raíz para que `pytest` encuentre los módulos del proyecto
- [x] Agregar `.gitignore` y subir el proyecto a GitHub
- [x] Renombrar `git.ignore` a `.gitignore` (con el nombre equivocado Git no ignoraba nada)
- [x] Sacar los archivos `.pyc` y `__pycache__` del repositorio

---

## ⏳ Tareas Pendientes

### 🗄️ Fase 4: Implementación con SQL Server
- [ ] **#9** `SqlServerSolicitudRepository` - Implementación con pyodbc. **En curso:**
  - [x] `obtener_por_id` (con prueba de integración)
  - [x] `guardar` con `INSERT` (asigna el id con `OUTPUT INSERTED.id`) y `UPDATE` (2 pruebas de integración en `tests/infrastructure/test_sql_server_solicitud_repository.py`)
  - [ ] `listar_por_estado` (hoy es un `raise NotImplementedError` provisional)
  - [ ] `listar_todas`, ordenada por `hora_solicitada` (provisional)
  - [ ] `eliminar`, devuelve `True`/`False` (provisional)
- [ ] **#10** `SqlServerServicioRepository` - Implementación con pyodbc

### 🌐 Fase 5: API REST
- [ ] **#5** Crear API con FastAPI (endpoints que delegan a casos de uso)

### 🧹 Pendientes menores
- [ ] Escribir `README.md` (qué hace el proyecto, cómo correr `pytest`, estructura de carpetas)
- [ ] Poner descripción y topics al repositorio de GitHub
- [ ] Notificar al cliente cuando el servicio pasa a PROXIMO_A_INICIAR (efecto de infraestructura, fuera del dominio)
- [ ] Implementar la regla de negocio de agendar solo entre las 6 am y las 4 pm (hoy nada la valida)
- [ ] Renombrar el parámetro `solicitud` a `servicio` en `guardar` de `ServicioRepository` y de `InMemoryServicioRepository`
- [ ] Separar los tests de integración (necesitan SQL Server encendido) de los unitarios, para poder correrlos por separado

---

## ⚠️ Deuda técnica conocida

- El test de `IniciarServicio` no detecta que falte la llamada a `guardar`, porque el repositorio en memoria guarda el mismo objeto. Revisar al implementar `SqlServerServicioRepository`, donde sí importará.
- `ConvertirSolicitudEnServicio` crea el servicio con `id=1` fijo. Con `IDENTITY` el id lo asigna la base, así que hay que crear el servicio con `id=None`. Corregir antes de la API o de `SqlServerServicioRepository`.
- Las entidades exigen un `id` al crearse, pero con `IDENTITY` las solicitudes y servicios nuevos nacen con `id=None`. Revisar `CrearSolicitud` y `ConvertirSolicitudEnServicio`.
- `IniciarServicio`, `MarcarServicioProximoAIniciar` y `FinalizarServicio` no validan que el servicio exista: si `obtener_por_id` no encuentra nada, el siguiente paso falla con un error poco claro. Agregar la validación (y su prueba) en los tres.
- `MostrarCitasHoy` usa `date.today()` por dentro, así que sus tests dependen de la fecha del sistema. Si hiciera falta, pasar la fecha como parámetro de `ejecutar`.
- En `SqlServerSolicitudRepository`, `obtener_por_id` usa `with` (que en `pyodbc` no cierra la conexión) y `guardar` usa `try/finally` con `close()`. Unificar al terminar los cinco métodos.

---

## 📊 Progreso General

```
Tareas completadas: 15/18 (83.3%)
Tareas pendientes:   3/18 (16.7%)
```

### Desglose por capa
```
Domain:          [██████████] 100% (5/5)
Infrastructure:  [█████░░░░░]  50% (2/4)
Application:     [██████████] 100% (8/8)
Presentation:    [░░░░░░░░░░]   0% (0/1)
```

---

## 📝 Notas

- Las fases siguen el orden lógico de implementación recomendado.
- Cada tarea debe incluir sus pruebas antes de marcarse como completada.
- Recordar actualizar este archivo al completar cada tarea.
- Ejecutar las pruebas con `pytest` desde la raíz (el archivo `pytest.ini` configura el path).
- Un commit por tarea: `pytest`, `git add` por nombre de archivo, `git commit -m "feat: ..."`, `git push`.
- Fase 3 (casos de uso de Servicio) cerrada.
- Fase 4 en curso: los tests de integración usan `LavadorasTestDB`, nunca la base real.