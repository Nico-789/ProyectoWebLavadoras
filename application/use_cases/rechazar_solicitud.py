from domain.repositories.solicitud_repository import SolicitudRepository
from application.dto.solicitud_dto import SolicitudDTO
from domain.enum.estadosolicitud import EstadoSolicitud
from domain.entities.solicitud import Solicitud
class RechazarSolicitud:
    def __init__(self, solicitud_repository: SolicitudRepository):
        self.solicitud_repository = solicitud_repository

    def ejecutar(self,solicitud_id):
            solicitudes = self.solicitud_repository.obtener_por_id(solicitud_id)
            solicitudes.rechazar()
            return self.solicitud_repository.guardar(solicitudes)
       
