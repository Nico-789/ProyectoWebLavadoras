import pytest
from infrastructure.repositories.in_memory_usuario_repository import InMemoryUsuarioRepository
from application.use_cases.crear_usuario import CrearUsuario
from tests.application.fakes import HasheadorFalso


@pytest.fixture
def repo():
    return InMemoryUsuarioRepository()


@pytest.fixture
def crear_usuario(repo):
    return CrearUsuario(repo, HasheadorFalso())


def test_crear_usuario_con_datos_validos_devuelve_el_nombre_de_usuario(crear_usuario,repo):
    resultado = crear_usuario.ejecutar("papa", "clave123")

    assert resultado == "papa"
    assert repo.obtener_por_nombre("papa")

def test_crear_usuario_con_password_vacia_lanza_value_error(crear_usuario,):
    with pytest.raises(ValueError):
        crear_usuario.ejecutar("papa", "")

def test_crear_usuario_con_nombre_repetido_lanza_value_error(crear_usuario):
    crear_usuario.ejecutar("papa", "clave123")
    with pytest.raises(ValueError):
        crear_usuario.ejecutar("papa", "otra123")