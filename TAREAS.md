# Tareas del Proyecto - ProyectoWebLavadoras

Roadmap de implementación organizado por fases. Se actualiza a medida que se completan tareas.

---

## ✅ Tareas Completadas

### Repositorio de Solicitud
- [x] Crear interfaz `SolicitudRepository` en `domain/repositories/`
- [x] Crear implementación `InMemorySolicitudRepository` en `infrastructure/repositories/`
- [x] Escribir pruebas del repositorio (8 pruebas, todas pasando)
- [x] Ejecutar y validar todas las pruebas (36/36 passing)

### Repositorio de Servicio
- [x] Crear interfaz `ServicioRepository` en `domain/repositories/`
- [x] Crear implementación `InMemoryServicioRepository` en `infrastructure/repositories/`
- [x] Escribir pruebas del repositorio de Servicio (6 pruebas, todas pasando)

### Casos de uso de Solicitud (Application Layer)
- [x] `CrearSolicitud` - Caso de uso para crear solicitudes (con prueba en `tests/application/test_crear_solicitud.py`)
- [x] `ListarSolicitudes` - Caso de uso para listar solicitudes, con orden cronológico
- [x] **#8** `RechazarSolicitud` - Caso de uso para rechazar solicitudes
- [x] **#13** `ConvertirSolicitudEnServicio` - Caso de uso para convertir solicitud en servicio

### Mantenimiento
- [x] Mover `test_rechazar_solicitud.py` a `tests/application/` y renombrar su test con un nombre descriptivo
- [x] Agregar `pytest.ini` en la raíz para que `pytest` encuentre los módulos del proyecto

---

## ⏳ Tareas Pendientes

### 📋 Fase 3: Casos de uso de Servicio
- [ ] **#15** `MostrarCitasHoy` - Caso de uso para listar servicios del día
- [ ] **#16** `IniciarServicio` - Caso de uso para iniciar un servicio
- [ ] **#17** `FinalizarServicio` - Caso de uso para finalizar un servicio

### 🗄️ Fase 4: Implementación con SQL Server
- [ ] **#9** `SqlServerSolicitudRepository` - Implementación con pyodbc
- [ ] **#10** `SqlServerServicioRepository` - Implementación con pyodbc

### 🌐 Fase 5: API REST
- [ ] **#5** Crear API con FastAPI (endpoints que delegan a casos de uso)

---

## 📊 Progreso General

```
Tareas completadas: 11/17 (64.7%)
Tareas pendientes:   6/17 (35.3%)
```

### Desglose por capa
```
Domain:          [██████████] 100% (5/5)
Infrastructure:  [█████░░░░░]  50% (2/4)
Application:     [██████░░░░]  57% (4/7)
Presentation:    [░░░░░░░░░░]   0% (0/1)
```

---

## 📝 Notas

- Las fases siguen el orden lógico de implementación recomendado.
- Cada tarea debe incluir sus pruebas antes de marcarse como completada.
- Recordar actualizar este archivo al completar cada tarea.
- Ejecutar las pruebas con `pytest` desde la raíz (el archivo `pytest.ini` configura el path).