import pyodbc
from domain.repositories.usuario_repository import UsuarioRepository
from domain.entities.usuario import Usuario


class SqlServerUsuarioRepository(UsuarioRepository):
    def __init__(self, connection_string: str):
        self._connection_string = connection_string

    def obtener_por_nombre(self, nombre_usuario: str) -> Usuario | None:
        with pyodbc.connect(self._connection_string) as conexion:
            fila = conexion.execute(
                "SELECT id, nombre_usuario, password_hash "
                "FROM Usuario WHERE nombre_usuario = ?",
                (nombre_usuario,),
            ).fetchone()

        if fila is None:
            return None

        return self._fila_a_usuario(fila)

    def guardar(self, usuario: Usuario) -> None:
        conexion = pyodbc.connect(self._connection_string)
        try:
            if usuario.id is None:
                cursor = conexion.execute(
                    "INSERT INTO Usuario (nombre_usuario, password_hash) "
                    "OUTPUT INSERTED.id "
                    "VALUES (?, ?)",
                    (usuario.nombre_usuario, usuario.password_hash),
                )
                usuario.id = cursor.fetchone()[0]
            else:
                conexion.execute(
                    "UPDATE Usuario SET nombre_usuario = ?, password_hash = ? WHERE id = ?",
                    (usuario.nombre_usuario, usuario.password_hash, usuario.id),
                )
            conexion.commit()
        except pyodbc.IntegrityError:
            # La restricción UNIQUE de la base rechazó el nombre repetido.
            # Se traduce al mismo error que lanza InMemoryUsuarioRepository.
            raise ValueError("Ya existe un usuario con ese nombre")
        finally:
            conexion.close()

    def _fila_a_usuario(self, fila) -> Usuario:
        return Usuario(
            id=fila.id,
            nombre_usuario=fila.nombre_usuario,
            password_hash=fila.password_hash,
        )