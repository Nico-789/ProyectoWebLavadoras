from domain.entities.solicitud import Solicitud
from domain.repositories.solicitud_repository import SolicitudRepository
from application.dto.solicitud_dto import SolicitudDTO
from domain.enum.estadosolicitud import EstadoSolicitud

class CrearSolicitud:
    def __init__(self, solicitud_repository: SolicitudRepository):
        self.solicitud_repository = solicitud_repository

    def ejecutar(self, dto: SolicitudDTO) -> Solicitud:
          solicitud = Solicitud(
              id=dto.id,
              id_electrodomestico=dto.id_electrodomestico,
              id_tipo_servicio=dto.id_tipo_servicio,
              problema=dto.problema,
              fecha_solicitada=dto.fecha_solicitada,
              hora_solicitada=dto.hora_solicitada,
              fecha=dto.fecha,
              hora_inicial=dto.hora_inicial,
              hora_final=dto.hora_final
          )
          self.solicitud_repository.guardar(solicitud)
          return solicitud