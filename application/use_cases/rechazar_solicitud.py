from application.exceptions import SolicitudNoEncontrada
from domain.repositories.solicitud_repository import SolicitudRepository


class RechazarSolicitud:
    def __init__(self, solicitud_repository: SolicitudRepository):
        self.solicitud_repository = solicitud_repository

    def ejecutar(self, solicitud_id):
        solicitud = self.solicitud_repository.obtener_por_id(solicitud_id)
        if solicitud is None:
            raise SolicitudNoEncontrada(solicitud_id)
        solicitud.rechazar()
        self.solicitud_repository.guardar(solicitud)
        return solicitud