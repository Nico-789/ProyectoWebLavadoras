class Usuario:
    def __init__(self, id, nombre_usuario, password_hash):
        if nombre_usuario is None or not nombre_usuario.strip():
            raise ValueError("El nombre de usuario no puede estar vacío")
        self.id = id
        self.nombre_usuario = nombre_usuario
        self.password_hash = password_hash