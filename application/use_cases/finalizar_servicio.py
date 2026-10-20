from domain.repositories.servicio_repository import ServicioRepository

class FinalizarServicio:
    def __init__(self, servicio_repository: ServicioRepository):
        self.servicio_repository= servicio_repository

    def ejecutar(self,servicio_id):
            servicio = self.servicio_repository.obtener_por_id(servicio_id)
            servicio.finalizar()
            return self.servicio_repository.guardar(servicio)