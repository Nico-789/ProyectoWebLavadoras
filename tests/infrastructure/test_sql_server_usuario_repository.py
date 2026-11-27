import os
import pytest
import pyodbc
from dotenv import load_dotenv
from infrastructure.repositories.sql_server_usuario_repository import SqlServerUsuarioRepository
from domain.entities.usuario import Usuario
load_dotenv()
CONNECTION_STRING = os.getenv("TEST_DB_CONNECTION_STRING")
class SqlServerUsuarioRepository(SqlServerUsuarioRepository):
    def __init__(self, connection_string: str):
        self._connection_string = connection_string

def crear_usuario(id=None, nombre_usuario="papa", password_hash="hash-de-prueba"):
    return Usuario(id=id, nombre_usuario=nombre_usuario, password_hash=password_hash)

@pytest.fixture
def repo():
    
    with pyodbc.connect(CONNECTION_STRING) as conexion:
        conexion.execute("DELETE FROM Usuario")
    return SqlServerUsuarioRepository(CONNECTION_STRING)

def test_guardar_asigna_id_y_obtener_por_nombre_lo_recupera(repo):
    usuario=crear_usuario()
    repo.guardar(usuario)
    encontrado=repo.obtener_por_nombre("papa")

    
    assert encontrado is not None
    assert encontrado.nombre_usuario == "papa"
    assert encontrado.password_hash == "hash-de-prueba"
    assert usuario.id == encontrado.id
    
def test_obtener_por_nombre_inexistente_por_otros_usuarios_devuelve_none(repo):
    usuario=crear_usuario()
    repo.guardar(usuario)
    encontrado=repo.obtener_por_nombre("mama")

    assert encontrado is None

def test_guardar_nombre_repetido_lanza_value_error(repo):
    usuario=crear_usuario()
    repo.guardar(usuario)

    usuario2=crear_usuario(password_hash="hash-deberas")

    with pytest.raises(ValueError, match="^Ya existe un usuario con ese nombre$"):
        repo.guardar(usuario2)

    encontrado=repo.obtener_por_nombre("papa")
    assert encontrado is not None
    assert usuario2.id is None

def test_guardar_usuario_existente_actualiza_la_contraseña_y_no_duplica(repo):
    usuario=crear_usuario()
    repo.guardar(usuario)

    usuario.password_hash="hash-deberas"
    repo.guardar(usuario)

    encontrado=repo.obtener_por_nombre("papa")
    assert encontrado.password_hash=="hash-deberas"
    assert encontrado.id == usuario.id


    

    
    




