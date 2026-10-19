from domain.enum.estadosolicitud import EstadoSolicitud
from domain.entities.solicitud import Solicitud
import pytest
from infrastructure.repositories.in_memory_solicitud_repository import InMemorySolicitudRepository
from datetime import date, time
from application.use_cases.crear_solicitud import CrearSolicitud
from application.dto.solicitud_dto import SolicitudDTO
@pytest.fixture
def repo():
    return InMemorySolicitudRepository()

def test_crear_solicitud_guarda_y_devuelve_la_solicitud(repo):
    dto=SolicitudDTO(
        id=1,
        id_electrodomestico=1,
        id_tipo_servicio=1,
        problema="No centrifuga",
        fecha_solicitada=date.today(),
        hora_solicitada=time(8,0),
        fecha=date.today(),
        hora_inicial=time(8, 0),
        hora_final=time(9, 0),
    )
    caso_uso=CrearSolicitud(repo)
    resultado=caso_uso.ejecutar(dto)
    encontrada = repo.obtener_por_id(1)
    
    
    assert resultado.id == 1
    assert resultado.problema == "No centrifuga"
    assert encontrada is not None
    assert encontrada.problema == "No centrifuga"
    assert resultado.estado == EstadoSolicitud.ENVIADA
  
    


    



