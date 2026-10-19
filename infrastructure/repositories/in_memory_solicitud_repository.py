from domain.repositories.solicitud_repository import SolicitudRepository
from domain.entities.solicitud import Solicitud
from domain.enum.estadosolicitud import EstadoSolicitud


class InMemorySolicitudRepository(SolicitudRepository):
    def __init__(self):
        self._solicitudes: dict[int, Solicitud] = {}

    def guardar(self, solicitud: Solicitud) -> None:
        self._solicitudes[solicitud.id] = solicitud

    def obtener_por_id(self, id: int) -> Solicitud | None:
        return self._solicitudes.get(id)

    def listar_por_estado(self, estado: EstadoSolicitud) -> list[Solicitud]:
        return [s for s in self._solicitudes.values() if s.estado == estado]

    def listar_todas(self) -> list[Solicitud]:
        return sorted(self._solicitudes.values(),key=lambda s:s.hora_solicitada)

    def eliminar(self, id: int) -> bool:
        return self._solicitudes.pop(id, None) is not None
