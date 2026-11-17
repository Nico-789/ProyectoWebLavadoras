from abc import ABC, abstractmethod
from domain.entities.usuario import Usuario


class UsuarioRepository(ABC):
    @abstractmethod
    def guardar(self, usuario: Usuario) -> None:
        ...

    @abstractmethod
    def obtener_por_nombre(self, nombre_usuario: str) -> Usuario | None:
        ...