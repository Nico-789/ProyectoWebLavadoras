# ProyectoWebLavadoras

Backend en Python para gestionar solicitudes y servicios de reparación de electrodomésticos de un negocio familiar. Está construido con **Clean Architecture** y **DDD**, con una suite de más de 80 pruebas automatizadas y una API REST con FastAPI.

## Qué hace

El cliente envía una **solicitud** de reparación. El negocio la revisa y puede **rechazarla** o **convertirla en un servicio** agendado. Cada servicio avanza por un ciclo de estados:

```
PENDIENTE → PROXIMO_A_INICIAR → EN_CURSO → FINALIZADO
```

Las transiciones inválidas (por ejemplo, iniciar un servicio que sigue pendiente) lanzan un error, y la API lo traduce a un `409`.

Ciclo de vida de una solicitud: `ENVIADA → EN_REVISION → RECHAZADA | CONVERTIDA_EN_SERVICIO`.

## Tecnologías

- Python 3.13
- FastAPI y Uvicorn (API REST)
- SQL Server Express con `pyodbc`
- pytest, `TestClient` de FastAPI y `httpx` (pruebas)
- Git y GitHub

## Estructura del proyecto

```
domain/
  entities/        Solicitud y Servicio, con sus reglas de negocio
  enum/            Estados de solicitud y de servicio
  repositories/    Interfaces de los repositorios
application/
  use_cases/       Un caso de uso por acción (crear, rechazar, convertir, iniciar...)
  dto/             Objetos de transferencia de datos
  exceptions.py    SolicitudNoEncontrada y ServicioNoEncontrado
infrastructure/
  repositories/    Implementaciones en memoria y en SQL Server
presentation/
  api/main.py      API con FastAPI
tests/             Pruebas unitarias, de integración y de la API
```

La regla de dependencias apunta hacia adentro: `domain` no conoce a nadie, `application` solo conoce a `domain`, y `infrastructure` y `presentation` dependen de las capas internas. Por eso los casos de uso reciben su repositorio por inyección, y las pruebas usan repositorios en memoria en vez de la base real.

## Cómo correrlo

### 1. Requisitos

- Python 3.13
- SQL Server Express (instancia `localhost\SQLEXPRESS`) y el driver **ODBC Driver 17 for SQL Server**

```powershell
pip install fastapi uvicorn pyodbc python-dotenv pytest httpx
```

### 2. Base de datos

Crea dos bases, `LavadorasDB` (la real) y `LavadorasTestDB` (solo para pruebas de integración), y en cada una las tablas `Solicitud` y `Servicio`, con `id INT IDENTITY(1,1) PRIMARY KEY`. El estado se guarda como texto.

### 3. Variables de entorno

Crea un archivo `.env` en la raíz (está en `.gitignore`, no se sube):

```
DB_CONNECTION_STRING=DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\SQLEXPRESS;DATABASE=LavadorasDB;Trusted_Connection=yes;
TEST_DB_CONNECTION_STRING=DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\SQLEXPRESS;DATABASE=LavadorasTestDB;Trusted_Connection=yes;
```

### 4. Levantar la API

```powershell
uvicorn presentation.api.main:app --reload
```

La documentación interactiva queda en `http://127.0.0.1:8000/docs`.

### 5. Correr las pruebas

```powershell
pytest
```

Los tests de integración (`tests/infrastructure/test_sql_server_*`) necesitan SQL Server encendido y borran las tablas de `LavadorasTestDB` antes de cada prueba. Nunca tocan la base real.

## Endpoints

| Método | Ruta | Qué hace |
|---|---|---|
| GET | `/health` | Comprobación de estado |
| GET | `/solicitudes` | Lista las solicitudes |
| POST | `/solicitudes` | Crea una solicitud (`201`) |
| POST | `/solicitudes/{id}/rechazar` | Rechaza una solicitud |
| POST | `/solicitudes/{id}/convertir` | La convierte en servicio (`201`) |
| POST | `/servicios/{id}/proximo-a-iniciar` | Servicio: pendiente → próximo a iniciar |
| POST | `/servicios/{id}/iniciar` | Servicio: próximo a iniciar → en curso |
| POST | `/servicios/{id}/finalizar` | Servicio: en curso → finalizado |
| GET | `/servicios/hoy` | Servicios agendados para hoy |

Errores: `404` si el recurso no existe y `409` si la transición de estado no es válida.

## Decisiones de diseño

- **Ids generados por la base.** Las entidades nacen con `id=None` y SQL Server los asigna con `IDENTITY`. Los repositorios en memoria imitan ese comportamiento.
- **Fecha de solicitud del lado del servidor.** El cliente no manda cuándo se hizo la solicitud; la API la fija al crearla.
- **Pruebas de mutación manuales.** Después de escribir cada prueba se altera el código a propósito para comprobar que la prueba falla cuando debe.
- **Excepciones de aplicación.** Los casos de uso lanzan `SolicitudNoEncontrada` o `ServicioNoEncontrado`, y la capa de presentación decide el código HTTP.

## Estado del proyecto

El avance y la deuda técnica conocida están en [`TAREAS.md`](TAREAS.md).