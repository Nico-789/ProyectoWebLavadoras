from domain.repositories.usuario_repository import UsuarioRepository
from domain.entities.usuario import Usuario


class InMemoryUsuarioRepository(UsuarioRepository):
    def __init__(self):
        self._usuarios: dict[int, Usuario] = {}

    def guardar(self, usuario: Usuario) -> None:
        # Imita el UNIQUE de la columna nombre_usuario en SQL Server.
        for existente in self._usuarios.values():
            if existente.nombre_usuario == usuario.nombre_usuario and existente.id != usuario.id:
                raise ValueError("Ya existe un usuario con ese nombre")
        if usuario.id is None:
            usuario.id = max(self._usuarios, default=0) + 1
        self._usuarios[usuario.id] = usuario

    def obtener_por_nombre(self, nombre_usuario: str) -> Usuario | None:
        for usuario in self._usuarios.values():
            if usuario.nombre_usuario == nombre_usuario:
                return usuario
        return None