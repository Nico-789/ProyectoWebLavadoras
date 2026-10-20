from datetime import date, datetime, time
from domain.repositories.servicio_repository import ServicioRepository


class MostrarCitasHoy:
    def __init__(self, servicio_repository: ServicioRepository):
        self.servicio_repository = servicio_repository

    def ejecutar(self):
        hoy = date.today()
        inicio = datetime.combine(hoy, time.min)
        fin = datetime.combine(hoy, time.max)
        return self.servicio_repository.listar_por_rango(inicio, fin)