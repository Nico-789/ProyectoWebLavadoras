from datetime import date, datetime, time, timedelta

import pytest
from fastapi.testclient import TestClient

from domain.entities.solicitud import Solicitud
from infrastructure.repositories.in_memory_solicitud_repository import InMemorySolicitudRepository
from presentation.api.main import app, obtener_repo_solicitudes
from domain.enum.estadosolicitud import EstadoSolicitud
from presentation.api.main import app, obtener_repo_servicios, obtener_repo_solicitudes
from infrastructure.repositories.in_memory_servicio_repository import InMemoryServicioRepository
from domain.entities.servicio import Servicio
from domain.enum.estadoservicio import estadoServicio


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

def crear_servicio(id, problema="No centrifuga", estado=estadoServicio.PENDIENTE,
    fecha_hora_inicio=datetime(2026, 8, 27, 10, 0)):
    return Servicio(
        id=id,
        id_electrodomestico=1,
        id_tipo_servicio=1,
        problema=problema,
        fecha_hora_inicio=fecha_hora_inicio,
        estado=estado,
    )


def test_marcar_servicio_proximo_a_iniciar_devuelve_el_nuevo_estado(client, repo_servicio):
    repo_servicio.guardar(crear_servicio(id=1))

    respuesta = client.post("/servicios/1/proximo-a-iniciar")

    assert respuesta.status_code == 200
    assert respuesta.json()["estado"] == "PROXIMO_A_INICIAR"


def test_iniciar_servicio_devuelve_estado_en_curso(client, repo_servicio):
    repo_servicio.guardar(crear_servicio(id=1, estado=estadoServicio.PROXIMO_A_INICIAR))

    respuesta = client.post("/servicios/1/iniciar")

    assert respuesta.status_code == 200
    assert respuesta.json()["estado"] == "EN_CURSO"
    assert respuesta.json()["fecha_hora_inicio_real"] is not None


def test_finalizar_servicio_devuelve_estado_finalizado(client, repo_servicio):
    servicio = crear_servicio(id=1)
    servicio.marcar_proximo_a_iniciar()
    servicio.iniciar()
    repo_servicio.guardar(servicio)

    respuesta = client.post("/servicios/1/finalizar")

    assert respuesta.status_code == 200
    assert respuesta.json()["estado"] == "FINALIZADO"
    assert respuesta.json()["duracion_real"] is not None


@pytest.mark.parametrize("accion", ["proximo-a-iniciar", "iniciar", "finalizar"])
def test_transicion_de_servicio_inexistente_devuelve_no_encontrado(client, accion):
    respuesta = client.post(f"/servicios/99999/{accion}")

    assert respuesta.status_code == 404


def test_iniciar_servicio_pendiente_devuelve_conflicto(client, repo_servicio):
    repo_servicio.guardar(crear_servicio(id=1))

    respuesta = client.post("/servicios/1/iniciar")

    assert respuesta.status_code == 409


def test_mostrar_citas_hoy_devuelve_solo_los_servicios_de_hoy(client, repo_servicio):
    repo_servicio.guardar(crear_servicio(id=1, problema="Hoy", fecha_hora_inicio=datetime.now()))
    repo_servicio.guardar(crear_servicio(id=2, problema="Pasado", fecha_hora_inicio=datetime.now() + timedelta(days=2)))

    respuesta = client.get("/servicios/hoy")

    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 1
    assert respuesta.json()[0]["problema"] == "Hoy"