from domain.enum.estadosolicitud import EstadoSolicitud
from domain.entities.solicitud import Solicitud
import pytest
from infrastructure.repositories.in_memory_solicitud_repository import InMemorySolicitudRepository
from datetime import date, time
from application.use_cases.listar_solicitudes import ListarSolicitudes

def crear_solicitud(id=1, problema="No centrifuga", estado=EstadoSolicitud.ENVIADA, hora_solicitada=None):
    return Solicitud(
        id=id,
        id_electrodomestico=1,
        id_tipo_servicio=1,
        problema=problema,
        fecha_solicitada=date.today(),
        hora_solicitada=hora_solicitada if hora_solicitada else time(),
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

def test_listar_solicitudes_devuelve_todas_las_solicitudes_en_orden_cronologico(repo):
    s1= crear_solicitud(hora_solicitada=time(8,0))
    s2 = crear_solicitud(id=2,hora_solicitada=time(10,0))
    s3 = crear_solicitud(id=3, estado=EstadoSolicitud.EN_REVISION,hora_solicitada=time(12,0))

    # Guardamos en desorden para probar el ordenamiento
    repo.guardar(s3) # 12:00
    repo.guardar(s1) # 8:00
    repo.guardar(s2) # 10:00

    caso_uso=ListarSolicitudes(repo)
    resultado=caso_uso.ejecutar()

    assert len(resultado) == 3
    assert resultado[0].hora_solicitada == time(8, 0)
    assert resultado[1].hora_solicitada == time(10, 0)
    assert resultado[2].hora_solicitada == time(12, 0)