import pytest
from application.interfaces.hasheador_password import HasheadorPassword
from domain.entities.usuario import Usuario
from infrastructure.repositories.in_memory_usuario_repository import InMemoryUsuarioRepository
from application.use_cases.iniciar_sesion import IniciarSesion
from application.interfaces.hasheador_password import HasheadorPassword

class HasheadorFalso(HasheadorPassword):
    def hashear(self, password):
        return f"hash-falso:{password}"

    def verificar(self, password, password_hash):
        return password_hash == self.hashear(password)

def crear_usuario(id=None, nombre_usuario="papa", password_hash="hash-de-prueba"):
    return Usuario(id=id, nombre_usuario=nombre_usuario, password_hash=password_hash)

@pytest.fixture
def repo():
    return InMemoryUsuarioRepository()

def test_iniciar_sesion_con_credenciales_correctas_devuelve_el_nombre_de_usuario(repo):
    hasheador = HasheadorFalso()
    repo.guardar(crear_usuario(password_hash=hasheador.hashear("clave123")))
    caso_uso = IniciarSesion(repo, hasheador)

    resultado = caso_uso.ejecutar("papa", "clave123")

    assert resultado == "papa"