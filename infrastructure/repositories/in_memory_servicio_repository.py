from domain.repositories.servicio_repository import ServicioRepository
from domain.entities.servicio import Servicio
from domain.enum.estadoservicio import estadoServicio
from datetime import datetime 

class InMemoryServicioRepository(ServicioRepository):
    def __init__(self):
        self._servicios: dict[int, Servicio] = {}
    
    def guardar(self, servicio: Servicio) -> None:
        self._servicios[servicio.id] = servicio

    def obtener_por_id(self, id: int) -> Servicio | None:
        return self._servicios.get(id)

    def listar_por_rango(self, fecha_hora_inicio:datetime,fecha_hora_fin:datetime) -> list[Servicio]:
        return [s for s in self._servicios.values() if fecha_hora_inicio <= s.fecha_hora_inicio <= fecha_hora_fin]

    def listar_todos(self) -> list[Servicio]:
        return list(self._servicios.values())
    
    def listar_por_estado(self, estado: estadoServicio) -> list[Servicio]:
        return [s for s in self._servicios.values() if s.estado == estado]

    def eliminar(self, id: int) -> bool:
        return self._servicios.pop(id, None) is not None