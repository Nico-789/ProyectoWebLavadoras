import pytest

from domain.entities.usuario import Usuario


def test_crear_usuario_guarda_sus_datos():
    usuario = Usuario(id=7, nombre_usuario="papa", password_hash="hash-de-prueba")

    assert usuario.id == 7
    assert usuario.nombre_usuario == "papa"
    assert usuario.password_hash == "hash-de-prueba"


@pytest.mark.parametrize("nombre", ["", "   "])
def test_crear_usuario_sin_nombre_lanza_error(nombre):
    with pytest.raises(ValueError, match="^El nombre de usuario no puede estar vacío$"):
        Usuario(id=None, nombre_usuario=nombre, password_hash="hash-de-prueba")