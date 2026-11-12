from domain.enum.estadosolicitud import EstadoSolicitud
from domain.entities.solicitud import Solicitud
import pytest
from infrastructure.repositories.in_memory_solicitud_repository import InMemorySolicitudRepository
from datetime import date, time
from application.use_cases.rechazar_solicitud import RechazarSolicitud
from application.exceptions import SolicitudNoEncontrada

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

def test_crear_solicitud_guarda_y_devuelve_la_solicitud(repo):
    s1=crear_solicitud(id=1,estado=EstadoSolicitud.EN_REVISION)
    repo.guardar(s1)
    caso_uso=RechazarSolicitud(repo)
    caso_uso.ejecutar(s1.id)

    solicitud_actualizada=repo.obtener_por_id(s1.id)
    assert solicitud_actualizada.estado==EstadoSolicitud.RECHAZADA

def test_rechazar_solicitud_inexistente_lanza_error():
    caso_uso = RechazarSolicitud(InMemorySolicitudRepository())

    with pytest.raises(SolicitudNoEncontrada):
        caso_uso.ejecutar(99999)

