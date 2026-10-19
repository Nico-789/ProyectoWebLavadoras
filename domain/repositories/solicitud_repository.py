from abc import ABC, abstractmethod
from domain.entities.solicitud import Solicitud
from domain.enum.estadosolicitud import EstadoSolicitud


class SolicitudRepository(ABC):
    @abstractmethod
    def guardar(self, solicitud: Solicitud) -> None:
        ...

    @abstractmethod
    def obtener_por_id(self, id: int) -> Solicitud | None:
        ...

    @abstractmethod
    def listar_por_estado(self, estado: EstadoSolicitud) -> list[Solicitud]:
        ...

    @abstractmethod
    def listar_todas(self) -> list[Solicitud]:
        ...

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        ...
