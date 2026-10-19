from domain.enum.estadoservicio import estadoServicio
from datetime import datetime, timedelta


class Servicio:
    def __init__(
        self,
        id,
        id_electrodomestico,
        id_tipo_servicio,
        problema,
        fecha_hora_inicio,
        estado=estadoServicio.PENDIENTE
    ):
        self.id = id
        self.id_electrodomestico = id_electrodomestico
        self.id_tipo_servicio = id_tipo_servicio
        self.problema = problema
        self.fecha_hora_inicio = fecha_hora_inicio

        self.duracion_estimada = 60
        self.fecha_hora_inicio_real = None
        self.fecha_hora_fin_real = None
        self.duracion_real = None

        self.estado = estado

        self.fecha_hora_fin = (
            fecha_hora_inicio + timedelta(minutes=self.duracion_estimada)
        )

    def marcar_proximo_a_iniciar(self):
        if self.estado == estadoServicio.PENDIENTE:
            self.estado = estadoServicio.PROXIMO_A_INICIAR
        else:
            raise ValueError(
                "No se puede marcar como próximo a iniciar "
                "un servicio que no está pendiente."
            )

    def iniciar(self):
        if self.estado == estadoServicio.PROXIMO_A_INICIAR:
            self.estado = estadoServicio.EN_CURSO
            self.fecha_hora_inicio_real = datetime.now()
        else:
            raise ValueError(
                "No se puede marcar un servicio en curso "
                "si no está próximo a iniciar."
            )

    def finalizar(self):
        if self.estado == estadoServicio.EN_CURSO:
            self.fecha_hora_fin_real = datetime.now()

            duracion = (
                self.fecha_hora_fin_real
                - self.fecha_hora_inicio_real
            )

            self.duracion_real = round(duracion.total_seconds() / 60)

            self.estado = estadoServicio.FINALIZADO
        else:
            raise ValueError(
                "No se puede marcar un servicio finalizado "
                "si no está en curso."
            )