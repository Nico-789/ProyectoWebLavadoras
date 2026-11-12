from datetime import datetime

from application.exceptions import SolicitudNoEncontrada
from domain.entities.servicio import Servicio
from domain.repositories.servicio_repository import ServicioRepository
from domain.repositories.solicitud_repository import SolicitudRepository


class ConvertirSolicitudEnServicio:
    def __init__(self, solicitud_repository: SolicitudRepository, servicio_repository: ServicioRepository):
        self.solicitud_repository = solicitud_repository
        self.servicio_repository = servicio_repository

    def ejecutar(self, solicitud_id):
        solicitud = self.solicitud_repository.obtener_por_id(solicitud_id)
        if solicitud is None:
            raise SolicitudNoEncontrada(solicitud_id)

        solicitud.convertir_en_servicio()

        nuevo_servicio = Servicio(
            id=None,
            id_electrodomestico=solicitud.id_electrodomestico,
            id_tipo_servicio=solicitud.id_tipo_servicio,
            problema=solicitud.problema,
            fecha_hora_inicio=datetime.combine(solicitud.fecha, solicitud.hora_inicial),
        )

        self.solicitud_repository.guardar(solicitud)
        self.servicio_repository.guardar(nuevo_servicio)
        return nuevo_servicio