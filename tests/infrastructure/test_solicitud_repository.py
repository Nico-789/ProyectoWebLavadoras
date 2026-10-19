from domain.enum.estadosolicitud import EstadoSolicitud
from domain.entities.solicitud import Solicitud
import pytest
from infrastructure.repositories.in_memory_solicitud_repository import InMemorySolicitudRepository
from datetime import date, time


def crear_solicitud(id=1, problema="No centrifuga", estado=EstadoSolicitud.ENVIADA):
    return Solicitud(
        id=id,
        id_electrodomestico=1,
        id_tipo_servicio=1,
        problema=problema,
        fecha_solicitada=date.today(),
        hora_solicitada=time(10, 0),
        fecha=date.today(),
        hora_inicial=time(8, 0),
        hora_final=time(9, 0),
        estado=estado,
    )


@pytest.fixture
def solicitud():
    return crear_solicitud()


@pytest.fixture
def repo():
    return InMemorySolicitudRepository()


def test_guardar_y_obtener_por_id(repo, solicitud):
    repo.guardar(solicitud)

    encontrada = repo.obtener_por_id(1)

    assert encontrada is not None
    assert encontrada.id == 1
    assert encontrada.problema == "No centrifuga"


def test_guardar_actualiza_si_id_existe(repo, solicitud):
    repo.guardar(solicitud)
    solicitud.poner_en_revision()
    repo.guardar(solicitud)

    encontrada = repo.obtener_por_id(1)
    assert encontrada.estado == EstadoSolicitud.EN_REVISION


def test_listar_por_estado(repo):
    s1 = crear_solicitud()
    s2 = crear_solicitud(id=2)
    s3 = crear_solicitud(id=3, estado=EstadoSolicitud.EN_REVISION)

    repo.guardar(s1)
    repo.guardar(s2)
    repo.guardar(s3)

    en_enviadas = repo.listar_por_estado(EstadoSolicitud.ENVIADA)

    assert len(en_enviadas) == 2
    assert all(s.estado == EstadoSolicitud.ENVIADA for s in en_enviadas)

    en_revision = repo.listar_por_estado(EstadoSolicitud.EN_REVISION)
    assert len(en_revision) == 1

def test_listar_por_estado_sin_resultados(repo):
    resultado = repo.listar_por_estado(EstadoSolicitud.ENVIADA)
    assert resultado == []


def test_listar_todas_con_resultados(repo):
    s1 = crear_solicitud()
    s2 = crear_solicitud(id=2)
    s3 = crear_solicitud(id=3)

    repo.guardar(s1)
    repo.guardar(s2)
    repo.guardar(s3)

    resultado = repo.listar_todas()

    assert len(resultado) == 3


def test_listar_todas_sin_resultados(repo):
    resultado = repo.listar_todas()
    assert resultado == []


def test_eliminar_existente(repo, solicitud):
    repo.guardar(solicitud)

    resultado = repo.eliminar(1)

    assert resultado is True
    assert repo.obtener_por_id(1) is None


def test_eliminar_inexistente(repo):
    resultado = repo.eliminar(99)
    assert resultado is False