# Tareas del Proyecto - ProyectoWebLavadoras

Roadmap de implementación organizado por fases. Se actualiza a medida que se completan tareas.

---

## ✅ Tareas Completadas

### Repositorio de Solicitud
- [x] Crear interfaz `SolicitudRepository` en `domain/repositories/`
- [x] Crear implementación `InMemorySolicitudRepository` en `infrastructure/repositories/` (asigna un id autoincremental cuando llega `id=None`, imitando `IDENTITY`)
- [x] Escribir pruebas del repositorio (9 pruebas, todas pasando)
- [x] Ejecutar y validar todas las pruebas (82/82 passing)

### Repositorio de Servicio
- [x] Crear interfaz `ServicioRepository` en `domain/repositories/`
- [x] Crear implementación `InMemoryServicioRepository` en `infrastructure/repositories/` (también asigna id autoincremental)
- [x] Escribir pruebas del repositorio de Servicio (6 pruebas, todas pasando)

### Casos de uso de Solicitud (Application Layer)
- [x] `CrearSolicitud` - Caso de uso para crear solicitudes (con prueba en `tests/application/test_crear_solicitud.py`)
- [x] `ListarSolicitudes` - Caso de uso para listar solicitudes, con orden cronológico
- [x] **#8** `RechazarSolicitud` - Rechaza solicitudes; lanza `SolicitudNoEncontrada` si no existe y devuelve la solicitud
- [x] **#13** `ConvertirSolicitudEnServicio` - Convierte solicitud en servicio; crea el servicio con `id=None` (lo asigna la base), lanza `SolicitudNoEncontrada` y devuelve el servicio. Con test espía que vigila el `id=None`

### Casos de uso de Servicio (Application Layer)
- [x] `MarcarServicioProximoAIniciar` - PENDIENTE → PROXIMO_A_INICIAR; lanza `ServicioNoEncontrado` y devuelve el servicio
- [x] **#16** `IniciarServicio` - PROXIMO_A_INICIAR → EN_CURSO; lanza `ServicioNoEncontrado` y devuelve el servicio
- [x] **#17** `FinalizarServicio` - EN_CURSO → FINALIZADO; lanza `ServicioNoEncontrado` y devuelve el servicio
- [x] **#15** `MostrarCitasHoy` - Lista servicios del día, de las 00:00 a las 23:59:59 de hoy
- [x] Excepciones de aplicación `SolicitudNoEncontrada` y `ServicioNoEncontrado` en `application/exceptions.py`

### Base de datos (Fase 4)
- [x] Verificar entorno: SQL Server Express (`localhost\SQLEXPRESS`), driver `ODBC Driver 17 for SQL Server` y `pyodbc`
- [x] Crear las bases `LavadorasDB` (real) y `LavadorasTestDB` (pruebas) con las tablas `Solicitud` y `Servicio` (id con `IDENTITY`)
- [x] Guardar las cadenas de conexión en `.env` (`DB_CONNECTION_STRING` y `TEST_DB_CONNECTION_STRING`), ignorado por Git
- [x] **#9** `SqlServerSolicitudRepository` - 5 métodos y 6 pruebas de integración, con método auxiliar `_fila_a_solicitud`
- [x] **#10** `SqlServerServicioRepository` - 6 métodos y 7 pruebas de integración, con método auxiliar `_fila_a_servicio`

### API REST (Fase 5)
- [x] **#5** API con FastAPI en `presentation/api/main.py`, con inyección de dependencias (`Depends`) y tests con `TestClient` usando repositorios en memoria (`tests/presentation/api/test_api_solicitudes.py`):
  - [x] `GET /health`
  - [x] `GET /solicitudes` y `POST /solicitudes` (201, la base asigna el id, la fecha y hora de solicitud las pone el servidor)
  - [x] `POST /solicitudes/{id}/rechazar` (404 si no existe, 409 si la transición no es válida)
  - [x] `POST /solicitudes/{id}/convertir` (201, devuelve el servicio creado)
  - [x] `POST /servicios/{id}/proximo-a-iniciar`, `/iniciar` y `/finalizar` (404 y 409)
  - [x] `GET /servicios/hoy`
- [x] Modelos Pydantic de entrada y respuesta en la capa de presentación (`SolicitudEntrada`, `SolicitudRespuesta`, `ServicioRespuesta`)
- [x] `SolicitudDTO` acepta `id=None`

### Mantenimiento
- [x] Mover `test_rechazar_solicitud.py` a `tests/application/` y renombrar su test con un nombre descriptivo
- [x] Agregar `pytest.ini` en la raíz para que `pytest` encuentre los módulos del proyecto
- [x] Agregar `.gitignore` y subir el proyecto a GitHub
- [x] Renombrar `git.ignore` a `.gitignore` (con el nombre equivocado Git no ignoraba nada)
- [x] Sacar los archivos `.pyc` y `__pycache__` del repositorio
- [x] Helpers de tests `crear_solicitud` (con `hora_solicitada`) y `crear_servicio`

---

## ⏳ Tareas Pendientes

### 🧹 Pendientes menores
- [ ] Escribir `README.md` (qué hace el proyecto, cómo correr `pytest`, cómo levantar la API con `uvicorn presentation.api.main:app --reload`, estructura de carpetas)
- [ ] Poner descripción y topics al repositorio de GitHub
- [ ] Hacer público el repositorio (hoy es privado): antes, confirmar que `.env` nunca entró al historial (`git log --all --oneline -- .env` debe salir vacío)
- [ ] Renombrar el test `test_eliminar_borra_la_solicitud_y_devuelve_true` del repositorio de Servicio a `..._borra_el_servicio_...`
- [ ] Renombrar el parámetro `solicitud` a `servicio` en `guardar` de `ServicioRepository` y de `InMemoryServicioRepository`
- [ ] Devolver las anotaciones de tipo en las firmas de los repositorios SQL
- [ ] Limpiar imports sin usar en los casos de uso (`ListarSolicitudes`, `CrearSolicitud`)
- [ ] Separar los tests de integración (necesitan SQL Server encendido) de los unitarios, para poder correrlos por separado
- [ ] Notificar al cliente cuando el servicio pasa a PROXIMO_A_INICIAR (efecto de infraestructura, fuera del dominio)
- [ ] Implementar la regla de negocio de agendar solo entre las 6 am y las 4 pm (hoy nada la valida)

### 🔭 Siguientes pasos posibles
- [ ] Probar la API de punta a punta contra SQL Server real (hoy sus tests usan repositorios en memoria)
- [ ] Endpoints de consulta que faltan: `GET /solicitudes/{id}`, `GET /servicios/{id}`, filtro por estado
- [ ] Tablas y llaves foráneas de `Electrodomestico` y `TipoServicio` (hoy los ids no se validan)
- [ ] Autenticación en la API

---

## ⚠️ Deuda técnica conocida

- `MostrarCitasHoy` usa `date.today()` por dentro, así que sus tests (y el de `GET /servicios/hoy`) dependen de la fecha del sistema. Si hiciera falta, pasar la fecha como parámetro de `ejecutar`.
- En los dos repositorios SQL, los métodos de lectura (`obtener_por_id` y los `listar_*`) usan `with` (que en `pyodbc` no cierra la conexión), mientras `guardar` y `eliminar` usan `try/finally` con `close()`. Unificar el estilo de conexión.
- Los tests de la API usan repositorios en memoria, que no imitan todo SQL Server (por ejemplo, el comportamiento de `IDENTITY` solo se prueba en los tests de integración).
- `CrearSolicitud` y los endpoints no validan que `id_electrodomestico` e `id_tipo_servicio` existan (no hay tablas ni llaves foráneas todavía).

---

## 📊 Progreso General

```
Tareas completadas: 18/18 (100%)
Tareas pendientes:   0/18 (0%)
Tests:              82/82 pasando
```

### Desglose por capa
```
Domain:          [██████████] 100% (5/5)
Infrastructure:  [██████████] 100% (4/4)
Application:     [██████████] 100% (8/8)
Presentation:    [██████████] 100% (1/1)
```

---