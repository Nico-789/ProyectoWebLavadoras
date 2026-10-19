from domain.enum.estadoservicio import estadoServicio
from domain.entities.servicio import Servicio
import pytest
from infrastructure.repositories.in_memory_servicio_repository import InMemoryServicioRepository
from datetime import datetime

def crear_servicio(id=1, problema="No centrifuga", estado=estadoServicio.PENDIENTE):
    return Servicio(
        id=id,
        id_electrodomestico=1,
        id_tipo_servicio=1,
        problema=problema,
        fecha_hora_inicio=datetime(2026, 8, 27, 10, 0),
        estado=estado,
)

@pytest.fixture
def servicio():
    return crear_servicio()

@pytest.fixture
def repo():
    return InMemoryServicioRepository()

def test_guardar_y_obtener_por_id(repo, servicio):
    repo.guardar(servicio)

    encontrada = repo.obtener_por_id(1)

    assert encontrada is not None
    assert encontrada.id == 1
    assert encontrada.problema == "No centrifuga"

def test_guardar_actualiza_si_id_existe(repo, servicio):
    repo.guardar(servicio)
    servicio.marcar_proximo_a_iniciar()
    repo.guardar(servicio)

    encontrada = repo.obtener_por_id(1)
    assert encontrada.estado == estadoServicio.PROXIMO_A_INICIAR

def test_listar_por_estado(repo):
    s1 = crear_servicio()
    s2 = crear_servicio(id=2)
    s3 = crear_servicio(id=3, estado=estadoServicio.PROXIMO_A_INICIAR)

    repo.guardar(s1)
    repo.guardar(s2)
    repo.guardar(s3)

    en_enviadas = repo.listar_por_estado(estadoServicio.PENDIENTE)

    assert len(en_enviadas) == 2
    assert all(s.estado == estadoServicio.PENDIENTE for s in en_enviadas)

    en_revision = repo.listar_por_estado(estadoServicio.PROXIMO_A_INICIAR)
    assert len(en_revision) == 1

def test_listar_por_estado_sin_resultados(repo):
    resultado = repo.listar_por_estado(estadoServicio.PROXIMO_A_INICIAR)
    assert resultado == []

def test_listar_todos_con_resultados(repo):
    s1 = crear_servicio()
    s2 = crear_servicio(id=2)
    s3 = crear_servicio(id=3)

    repo.guardar(s1)
    repo.guardar(s2)
    repo.guardar(s3)

    resultado = repo.listar_todos()

    assert len(resultado) == 3

def test_listar_todas_sin_resultados(repo):
    resultado = repo.listar_todos()
    assert resultado == []

