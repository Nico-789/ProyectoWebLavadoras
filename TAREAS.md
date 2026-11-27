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

### Login para tu papá (Fase 6, avance)
- [x] **#1** Entidad `Usuario` (`id`, `nombre_usuario`, `password_hash`); un nombre vacío o solo con espacios lanza `ValueError` (3 pruebas)
- [x] **#2** `UsuarioRepository` en `domain/repositories/` e `InMemoryUsuarioRepository` con `obtener_por_nombre` y `guardar` (id autoincremental y nombre único, que lanza `ValueError`). 6 pruebas. `obtener_por_id` se dejó fuera a propósito: ningún caso de uso lo necesita
- [x] **#3** Hasheo de contraseñas: interfaz `HasheadorPassword` en `application/interfaces/` y `Argon2Hasheador` en `infrastructure/security/` (librería `argon2-cffi`, sin criptografía propia). 5 pruebas
- [x] **#4** Caso de uso `IniciarSesion` y excepción `CredencialesInvalidas` (sin parámetros, mensaje fijo). Usuario inexistente y contraseña mala lanzan exactamente el mismo error. Devuelve el `nombre_usuario`. 3 pruebas con un hasheador falso
- [x] **#5 (parcial)** Tabla `Usuario` con `UNIQUE` en `nombre_usuario` en `LavadorasDB` y `LavadorasTestDB`; `SqlServerUsuarioRepository` (`INSERT`, `UPDATE`, y el `IntegrityError` de la base se traduce al mismo `ValueError` que lanza el repositorio en memoria). 4 pruebas de integración: guardar y recuperar, nombre inexistente, nombre repetido y actualización sin duplicar
- [x] Mutation testing manual aplicado a `Usuario`, `InMemoryUsuarioRepository`, `Argon2Hasheador`, `IniciarSesion` y al repositorio SQL

### Mantenimiento
- [x] Mover `test_rechazar_solicitud.py` a `tests/application/` y renombrar su test con un nombre descriptivo
- [x] Agregar `pytest.ini` en la raíz para que `pytest` encuentre los módulos del proyecto
- [x] Agregar `.gitignore` y subir el proyecto a GitHub
- [x] Renombrar `git.ignore` a `.gitignore` (con el nombre equivocado Git no ignoraba nada)
- [x] Sacar los archivos `.pyc` y `__pycache__` del repositorio
- [x] Helpers de tests `crear_solicitud` (con `hora_solicitada`) y `crear_servicio`

---

## ⏳ Tareas Pendientes

### 🔐 Login para tu papá (lo que falta)
- [ ] **#5** Script para crear el usuario de tu papá: la contraseña no queda en el código ni en Git (decidir si se pide por consola o desde una variable de entorno); usa `Argon2Hasheador` y `SqlServerUsuarioRepository`
- [ ] **#6** Sesión con cookie en la API:
  - [ ] Decidir cookie firmada o JWT (recomendado para este panel: cookie firmada, con solo el `nombre_usuario` adentro)
  - [ ] `POST /login` que fija la cookie firmada y con vencimiento
  - [ ] `POST /logout`
  - [ ] Clave secreta de la sesión en `.env`
  - [ ] Tests: cookie al entrar bien, nada al entrar mal
- [ ] **#7** Proteger los endpoints del panel:
  - [ ] Dependencia que exige sesión y responde `401` si no la hay
  - [ ] Aplicarla a listar, rechazar, convertir, las tres transiciones de servicio y `GET /servicios/hoy`
  - [ ] Dejar públicos `POST /solicitudes` y `/health`
  - [ ] Tests: cada endpoint protegido responde `401` sin sesión
  - [ ] Actualizar los tests actuales de la API, que hoy no mandan sesión
- [ ] **#8** Límite de intentos de login, para frenar adivinar contraseñas
- [ ] Opcional: igualar el tiempo de respuesta entre usuario inexistente y contraseña mala (hoy el primero responde más rápido porque no calcula ningún hash)
- [ ] Decidir si `IniciarSesion` devuelve `usuario.nombre_usuario` en vez del parámetro recibido
- [ ] Limpieza del login: renombrar `tests/application/test_aplication.py` a `test_iniciar_sesion.py`, borrar el import de `Usuario` sin usar en `iniciar_sesion.py`, guardar `scripts/crear_tabla_usuario.sql` en el repo y crear `requirements.txt` (con `argon2-cffi`)

### 📝 Formulario del cliente
- [ ] **#1** Datos del cliente en la solicitud (hoy no se guarda quién la envía):
  - [ ] Agregar `nombre_cliente` y `telefono_cliente` a la entidad `Solicitud`, a `SolicitudDTO` y a `CrearSolicitud`
  - [ ] Agregar las dos columnas a la tabla `Solicitud` en las dos bases
  - [ ] Ajustar `SqlServerSolicitudRepository` (`INSERT`, `UPDATE`, `SELECT` y `_fila_a_solicitud`)
  - [ ] Ajustar los modelos de la API y los tests existentes
  - [ ] Validar que el nombre y el teléfono no vengan vacíos y que el teléfono tenga un formato válido
- [ ] **#2** Revisar `POST /solicitudes`: validaciones de longitud y de fecha (que no sea pasada)
- [ ] **#3** Página del formulario servida por la propia API (electrodoméstico, problema, día, hora, nombre y teléfono):
  - [ ] Mensaje de confirmación al enviar
  - [ ] Mensajes claros de error
  - [ ] Que se vea bien desde el celular
- [ ] **#4** Protección contra basura en el formulario público: límite de envíos por dirección y campo oculto trampa (honeypot)
- [ ] **#5** Aviso de datos personales en el formulario, diciendo para qué se usan el nombre y el teléfono
- [ ] **#6** Tests: el formulario envía bien, rechaza datos inválidos y la solicitud queda guardada

### 🧭 Decisiones pendientes
- Cómo se llena el electrodoméstico y el tipo de servicio: hoy son dos ids sueltos sin tablas que los definan; el formulario necesita una lista fija o esas tablas
- Que el horario permitido (6 am a 4 pm) quede validado en el formulario (ver también la regla de negocio en los pendientes menores)
- Cookie firmada o JWT para la sesión (punto 6 del login)

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

---

## ⚠️ Deuda técnica conocida

- `MostrarCitasHoy` usa `date.today()` por dentro, así que sus tests (y el de `GET /servicios/hoy`) dependen de la fecha del sistema. Si hiciera falta, pasar la fecha como parámetro de `ejecutar`.
- En los dos repositorios SQL, los métodos de lectura (`obtener_por_id` y los `listar_*`) usan `with` (que en `pyodbc` no cierra la conexión), mientras `guardar` y `eliminar` usan `try/finally` con `close()`. Unificar el estilo de conexión.
- Los tests de la API usan repositorios en memoria, que no imitan todo SQL Server (por ejemplo, el comportamiento de `IDENTITY` solo se prueba en los tests de integración).
- `CrearSolicitud` y los endpoints no validan que `id_electrodomestico` e `id_tipo_servicio` existan (no hay tablas ni llaves foráneas todavía).
- `InMemoryUsuarioRepository` distingue mayúsculas (`papa` y `Papa` son usuarios distintos) y SQL Server, con su configuración habitual, no. Los dos repositorios se comportan distinto en ese punto.
- `SqlServerUsuarioRepository` traduce cualquier `IntegrityError` a "Ya existe un usuario con ese nombre". Hoy el único motivo posible es el `UNIQUE`, pero si apareciera otra restricción el mensaje sería engañoso.
- Un `UPDATE` sobre un id que no existe no falla ni crea nada en SQL Server; el repositorio en memoria lo crearía.

---

## 📊 Progreso General

```
Tests:              103/103 pasando
Login para tu papá: 4 de 8 puntos completos, el 5 va a la mitad
Formulario cliente: 0 de 6 puntos
```

### Desglose por capa (las capas originales)
```
Domain:          [██████████] 100% (5/5)
Infrastructure:  [██████████] 100% (4/4)
Application:     [██████████] 100% (8/8)
Presentation:    [██████████] 100% (1/1)
```

---