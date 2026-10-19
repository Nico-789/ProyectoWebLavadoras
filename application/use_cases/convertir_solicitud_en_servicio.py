from domain.repositories.solicitud_repository import SolicitudRepository
from domain.repositories.servicio_repository import ServicioRepository
from domain.entities.servicio import Servicio
from datetime import datetime

class ConvertirSolicitudEnServicio:
    def __init__(self, solicitud_repository: SolicitudRepository, servicio_repository: ServicioRepository):
        self.solicitud_repository = solicitud_repository
        self.servicio_repository = servicio_repository

    def ejecutar(self, solicitud_id):
        # 1. Recuperar la solicitud
        solicitud = self.solicitud_repository.obtener_por_id(solicitud_id)

        # 2. Ejecutar la regla de negocio de la entidad
        solicitud.convertir_en_servicio()

        # 3. Crear el nuevo Servicio usando la información de la solicitud
        # Combinamos la fecha y la hora de la solicitud para crear el datetime que pide Servicio
        nuevo_servicio = Servicio(
            id=1,
            id_electrodomestico=solicitud.id_electrodomestico,
            id_tipo_servicio=solicitud.id_tipo_servicio,
            problema=solicitud.problema,
            fecha_hora_inicio=datetime.combine(solicitud.fecha, solicitud.hora_inicial)
        )

        # 4. Persistir ambos cambios
        self.solicitud_repository.guardar(solicitud)
        self.servicio_repository.guardar(nuevo_servicio)
