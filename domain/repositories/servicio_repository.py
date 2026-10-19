from abc import ABC, abstractmethod
from domain.entities.servicio import Servicio
from domain.enum.estadoservicio import estadoServicio
from datetime import datetime 

class ServicioRepository(ABC):

    @abstractmethod
    def guardar(self, solicitud: Servicio) -> None:
        ...
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Servicio | None:
        ...

    @abstractmethod
    def listar_todos(self)-> list[Servicio]:
        ...

    @abstractmethod
    def listar_por_estado(self, estado: estadoServicio) -> list[Servicio]:
        ...

    @abstractmethod
    def listar_por_rango(self, fecha_hora_inicio:datetime,fecha_hora_fin:datetime) -> list[Servicio]:
        ...
        
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        ...
