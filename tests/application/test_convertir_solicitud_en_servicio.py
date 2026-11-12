from domain.enum.estadosolicitud import EstadoSolicitud
from domain.entities.solicitud import Solicitud
import pytest
from infrastructure.repositories.in_memory_solicitud_repository import InMemorySolicitudRepository
from datetime import date, time
from infrastructure.repositories.in_memory_servicio_repository import InMemoryServicioRepository
from application.use_cases.convertir_solicitud_en_servicio import ConvertirSolicitudEnServicio
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
def repo_solicitud():
    return InMemorySolicitudRepository()

@pytest.fixture
def repo_servicio():
    return InMemoryServicioRepository()

def test_convertir_solicitud_en_servicio_exitosa(repo_solicitud,repo_servicio):
    s1=crear_solicitud(id=1,estado=EstadoSolicitud.EN_REVISION)
    repo_solicitud.guardar(s1)
    caso_uso = ConvertirSolicitudEnServicio(repo_solicitud, repo_servicio)
    caso_uso.ejecutar(s1.id)

    solicitud_actualizada=repo_solicitud.obtener_por_id(s1.id)
    assert solicitud_actualizada.estado == EstadoSolicitud.CONVERTIDA_EN_SERVICIO
    assert len(repo_servicio.listar_todos()) == 1

class ServicioRepositorySpy(InMemoryServicioRepository):
    def __init__(self):
        super().__init__()
        self.ids_recibidos = []

    def guardar(self, servicio):
        self.ids_recibidos.append(servicio.id)
        super().guardar(servicio)


def test_convertir_crea_el_servicio_con_id_none_para_que_lo_asigne_la_base(repo_solicitud):
    repo_servicio = ServicioRepositorySpy()
    s1 = crear_solicitud(id=1, estado=EstadoSolicitud.EN_REVISION)
    repo_solicitud.guardar(s1)
    caso_uso = ConvertirSolicitudEnServicio(repo_solicitud, repo_servicio)

    caso_uso.ejecutar(s1.id)

    assert repo_servicio.ids_recibidos == [None]

def test_convertir_solicitud_inexistente_lanza_error(repo_solicitud, repo_servicio):
    caso_uso = ConvertirSolicitudEnServicio(repo_solicitud, repo_servicio)

    with pytest.raises(SolicitudNoEncontrada):
        caso_uso.ejecutar(99999)


def test_convertir_devuelve_el_servicio_creado(repo_solicitud, repo_servicio):
    s1 = crear_solicitud(id=1, estado=EstadoSolicitud.EN_REVISION)
    repo_solicitud.guardar(s1)

    servicio = ConvertirSolicitudEnServicio(repo_solicitud, repo_servicio).ejecutar(s1.id)

    assert servicio.problema == "No centrifuga"
    assert servicio.id is not None