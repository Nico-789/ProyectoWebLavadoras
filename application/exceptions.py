class SolicitudNoEncontrada(Exception):
    def __init__(self, solicitud_id):
        super().__init__(f"No existe la solicitud con id {solicitud_id}")
        self.solicitud_id = solicitud_id