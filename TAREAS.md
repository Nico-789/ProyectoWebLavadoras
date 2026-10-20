# Tareas del Proyecto - ProyectoWebLavadoras

Roadmap de implementación organizado por fases. Se actualiza a medida que se completan tareas.

---

## ✅ Tareas Completadas

### Repositorio de Solicitud
- [x] Crear interfaz `SolicitudRepository` en `domain/repositories/`
- [x] Crear implementación `InMemorySolicitudRepository` en `infrastructure/repositories/`
- [x] Escribir pruebas del repositorio (8 pruebas, todas pasando)
- [x] Ejecutar y validar todas las pruebas (40/40 passing)

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

### Mantenimiento
- [x] Mover `test_rechazar_solicitud.py` a `tests/application/` y renombrar su test con un nombre descriptivo
- [x] Agregar `pytest.ini` en la raíz para que `pytest` encuentre los módulos del proyecto
- [x] Agregar `.gitignore` y subir el proyecto a GitHub

---

## ⏳ Tareas Pendientes

### 📋 Fase 3: Casos de uso de Servicio
Se siguen en el orden del ciclo de estados: `PENDIENTE → PROXIMO_A_INICIAR → EN_CURSO → FINALIZADO`

- [ ] **#17** `FinalizarServicio` - Caso de uso para pasar un servicio de EN_CURSO a FINALIZADO
- [ ] **#15** `MostrarCitasHoy` - Caso de uso para listar servicios del día (usa `listar_por_rango`)

### 🗄️ Fase 4: Implementación con SQL Server
- [ ] **#9** `SqlServerSolicitudRepository` - Implementación con pyodbc
- [ ] **#10** `SqlServerServicioRepository` - Implementación con pyodbc

### 🌐 Fase 5: API REST
- [ ] **#5** Crear API con FastAPI (endpoints que delegan a casos de uso)

### 🧹 Pendientes menores
- [ ] Escribir `README.md` (qué hace el proyecto, cómo correr `pytest`, estructura de carpetas)
- [ ] Poner descripción y topics al repositorio de GitHub
- [ ] Notificar al cliente cuando el servicio pasa a PROXIMO_A_INICIAR (efecto de infraestructura, fuera del dominio)

---

## ⚠️ Deuda técnica conocida

- El test de `IniciarServicio` no detecta que falte la llamada a `guardar`, porque el repositorio en memoria guarda el mismo objeto. Revisar al implementar SQL Server.
- `ConvertirSolicitudEnServicio` crea el servicio con `id=1` fijo. Con varios servicios se pisarían entre sí. Corregir antes de la API o de SQL Server.
- `IniciarServicio` y `MarcarServicioProximoAIniciar` no validan que el servicio exista: si `obtener_por_id` no encuentra nada, el siguiente paso falla con un error poco claro. Agregar la validación (y su prueba) en ambos y en los casos de uso de Servicio que vengan.

---

## 📊 Progreso General

```
Tareas completadas: 13/18 (72.2%)
Tareas pendientes:   5/18 (27.8%)
```

### Desglose por capa
```
Domain:          [██████████] 100% (5/5)
Infrastructure:  [█████░░░░░]  50% (2/4)
Application:     [███████░░░]  75% (6/8)
Presentation:    [░░░░░░░░░░]   0% (0/1)
```

---

## 📝 Notas

- Las fases siguen el orden lógico de implementación recomendado.
- Cada tarea debe incluir sus pruebas antes de marcarse como completada.
- Recordar actualizar este archivo al completar cada tarea.
- Ejecutar las pruebas con `pytest` desde la raíz (el archivo `pytest.ini` configura el path).
- Un commit por tarea: `pytest`, `git add .`, `git commit -m "feat: ..."`, `git push`.