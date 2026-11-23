class SolicitudNoEncontrada(Exception):
    def __init__(self, solicitud_id):
        super().__init__(f"No existe la solicitud con id {solicitud_id}")
        self.solicitud_id = solicitud_id

class ServicioNoEncontrado(Exception):
    def __init__(self, servicio_id):
        super().__init__(f"No existe el servicio con id {servicio_id}")
        self.servicio_id = servicio_id

class CredencialesInvalidas(Exception):
    def __init__(self):
        super().__init__("USUARIO O CONTRASEÑA INCORRECTOS")

