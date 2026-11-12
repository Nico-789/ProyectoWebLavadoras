from datetime import date, time

import pytest
from fastapi.testclient import TestClient

from domain.entities.solicitud import Solicitud
from infrastructure.repositories.in_memory_solicitud_repository import InMemorySolicitudRepository
from presentation.api.main import app, obtener_repo_solicitudes
from domain.enum.estadosolicitud import EstadoSolicitud
from presentation.api.main import app, obtener_repo_servicios, obtener_repo_solicitudes
from infrastructure.repositories.in_memory_servicio_repository import InMemoryServicioRepository


@pytest.fixture
def repo():
    return InMemorySolicitudRepository()


@pytest.fixture
def repo_servicio():
    return InMemoryServicioRepository()


@pytest.fixture
def client(repo, repo_servicio):
    app.dependency_overrides[obtener_repo_solicitudes] = lambda: repo
    app.dependency_overrides[obtener_repo_servicios] = lambda: repo_servicio
    yield TestClient(app)
    app.dependency_overrides.clear()

def test_health_responde_ok(client):
    respuesta = client.get("/health")

    assert respuesta.status_code == 200
    assert respuesta.json() == {"estado": "ok"}


def test_listar_solicitudes_devuelve_las_guardadas(client, repo):
    repo.guardar(Solicitud(
        id=1,
        id_electrodomestico=1,
        id_tipo_servicio=1,
        problema="No centrifuga",
        fecha_solicitada=date.today(),
        hora_solicitada=time(10, 0),
        fecha=date.today(),
        hora_inicial=time(8, 0),
        hora_final=time(9, 0),
    ))

    respuesta = client.get("/solicitudes")

    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 1
    assert respuesta.json()[0]["problema"] == "No centrifuga"


def test_crear_solicitud_devuelve_201_y_asigna_id(client, repo):
    cuerpo = {
        "id_electrodomestico": 1,
        "id_tipo_servicio": 1,
        "problema": "No centrifuga",
        "fecha": "2026-11-20",
        "hora_inicial": "08:00:00",
        "hora_final": "09:00:00",
    }

    respuesta = client.post("/solicitudes", json=cuerpo)

    assert respuesta.status_code == 201
    assert respuesta.json()["estado"] == "ENVIADA"
    assert repo.obtener_por_id(respuesta.json()["id"]) is not None

def crear_solicitud(id, estado=EstadoSolicitud.ENVIADA):
    return Solicitud(
        id=id,
        id_electrodomestico=1,
        id_tipo_servicio=1,
        problema="No centrifuga",
        fecha_solicitada=date.today(),
        hora_solicitada=time(10, 0),
        fecha=date.today(),
        hora_inicial=time(8, 0),
        hora_final=time(9, 0),
        estado=estado,
    )

def test_rechazar_solicitud_en_revision_devuelve_estado_rechazada(client, repo):
    repo.guardar(crear_solicitud(id=1, estado=EstadoSolicitud.EN_REVISION))

    respuesta = client.post("/solicitudes/1/rechazar")

    assert respuesta.status_code == 200
    assert respuesta.json()["estado"] == "RECHAZADA"


def test_rechazar_solicitud_inexistente_devuelve_error_no_encontrado(client):
    respuesta = client.post("/solicitudes/99999/rechazar")

    assert respuesta.status_code == 404


def test_rechazar_solicitud_ya_rechazada_devuelve_conflicto(client, repo):
    repo.guardar(crear_solicitud(id=1, estado=EstadoSolicitud.RECHAZADA))

    respuesta = client.post("/solicitudes/1/rechazar")

    assert respuesta.status_code == 409

def test_convertir_solicitud_en_revision_crea_un_servicio_pendiente(client, repo, repo_servicio):
    repo.guardar(crear_solicitud(id=1, estado=EstadoSolicitud.EN_REVISION))

    respuesta = client.post("/solicitudes/1/convertir")

    assert respuesta.status_code == 201
    assert respuesta.json()["estado"] == "PENDIENTE"
    assert repo.obtener_por_id(1).estado == EstadoSolicitud.CONVERTIDA_EN_SERVICIO
    assert len(repo_servicio.listar_todos()) == 1


def test_convertir_solicitud_inexistente_devuelve_error_no_encontrado(client):
    respuesta = client.post("/solicitudes/99999/convertir")

    assert respuesta.status_code == 404


def test_convertir_solicitud_sin_revisar_devuelve_conflicto(client, repo):
    repo.guardar(crear_solicitud(id=1, estado=EstadoSolicitud.ENVIADA))

    respuesta = client.post("/solicitudes/1/convertir")

    assert respuesta.status_code == 409