from domain.enum.estadosolicitud import EstadoSolicitud
class Solicitud:
    def __init__(self,id,id_electrodomestico,id_tipo_servicio,problema,fecha_solicitada,hora_solicitada,fecha,hora_inicial,hora_final,estado=EstadoSolicitud.ENVIADA):
        self.id=id
        self.id_electrodomestico=id_electrodomestico
        self.id_tipo_servicio=id_tipo_servicio
        self.problema=problema
        self.fecha_solicitada=fecha_solicitada
        self.hora_solicitada=hora_solicitada
        self.fecha=fecha
        self.hora_inicial=hora_inicial
        self.hora_final=hora_final
        self.estado = estado

    def poner_en_revision(self):
        if self.estado != EstadoSolicitud.ENVIADA:
            raise ValueError(
                "Solo se puede poner en revisión una solicitud que está enviada."
            )
        self.estado = EstadoSolicitud.EN_REVISION

    def rechazar(self):
        if self.estado != EstadoSolicitud.EN_REVISION:
            raise ValueError(
                "Solo se puede rechazar una solicitud que está en revisión."
            )
        self.estado = EstadoSolicitud.RECHAZADA

    def convertir_en_servicio(self):
        if self.estado != EstadoSolicitud.EN_REVISION:
            raise ValueError(
                "Solo se puede convertir en servicio una solicitud que está en revisión."
            )
        self.estado = EstadoSolicitud.CONVERTIDA_EN_SERVICIO
        return self