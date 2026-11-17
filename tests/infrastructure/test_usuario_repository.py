import pytest

from domain.entities.usuario import Usuario
from infrastructure.repositories.in_memory_usuario_repository import InMemoryUsuarioRepository


def crear_usuario(id=None, nombre_usuario="papa", password_hash="hash-de-prueba"):
    return Usuario(id=id, nombre_usuario=nombre_usuario, password_hash=password_hash)


@pytest.fixture
def repo():
    return InMemoryUsuarioRepository()


def test_guardar_y_obtener_por_nombre(repo):
    repo.guardar(crear_usuario())

    encontrado = repo.obtener_por_nombre("papa")

    assert encontrado is not None
    assert encontrado.nombre_usuario == "papa"
    assert encontrado.password_hash == "hash-de-prueba"


def test_obtener_por_nombre_inexistente_devuelve_none(repo):
    assert repo.obtener_por_nombre("nadie") is None


def test_obtener_por_nombre_inexistente_con_otros_usuarios_devuelve_none(repo):
    repo.guardar(crear_usuario(nombre_usuario="mama"))

    assert repo.obtener_por_nombre("papa") is None


def test_guardar_con_id_none_asigna_id_autoincremental(repo):
    primero = crear_usuario(nombre_usuario="papa")
    segundo = crear_usuario(nombre_usuario="mama")

    repo.guardar(primero)
    repo.guardar(segundo)

    assert primero.id == 1
    assert segundo.id == 2


def test_guardar_nombre_repetido_lanza_error(repo):
    repo.guardar(crear_usuario(nombre_usuario="papa"))

    with pytest.raises(ValueError, match="^Ya existe un usuario con ese nombre$"):
        repo.guardar(crear_usuario(nombre_usuario="papa"))


def test_guardar_el_mismo_usuario_otra_vez_lo_actualiza(repo):
    usuario = crear_usuario()
    repo.guardar(usuario)

    usuario.password_hash = "hash-nuevo"
    repo.guardar(usuario)

    assert repo.obtener_por_nombre("papa").password_hash == "hash-nuevo"