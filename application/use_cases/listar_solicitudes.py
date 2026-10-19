from domain.repositories.solicitud_repository import SolicitudRepository
from application.dto.solicitud_dto import SolicitudDTO
from domain.enum.estadosolicitud import EstadoSolicitud

class ListarSolicitudes:
    def __init__(self, solicitud_repository: SolicitudRepository):
        self.solicitud_repository = solicitud_repository

    def ejecutar(self):
        solicitudes = self.solicitud_repository.listar_todas()
        return solicitudes
