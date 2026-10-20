from domain.repositories.servicio_repository import ServicioRepository


class MarcarServicioProximoAIniciar:
    def __init__(self, servicio_repository: ServicioRepository):
        self.servicio_repository = servicio_repository

    def ejecutar(self, servicio_id):
        servicio = self.servicio_repository.obtener_por_id(servicio_id)
        servicio.marcar_proximo_a_iniciar()
        return self.servicio_repository.guardar(servicio)