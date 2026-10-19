from domain.enum.estadoservicio import estadoServicio
from domain.entities.servicio import Servicio
import pytest
from infrastructure.repositories.in_memory_servicio_repository import InMemoryServicioRepository
from datetime import datetime
from application.use_cases.iniciar_servicio import IniciarServicio
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

def test_iniciar_servicio_cambia_el_estado_a_en_curso(repo,servicio):
    servicio.marcar_proximo_a_iniciar()
    repo.guardar(servicio)
    caso_uso=IniciarServicio(repo)
    caso_uso.ejecutar(servicio.id)
    encontrada = repo.obtener_por_id(servicio.id)

    
    assert encontrada is not None
    assert encontrada.fecha_hora_inicio_real is not None
    assert encontrada.estado == estadoServicio.EN_CURSO

def test_iniciar_servicio_pendiente_lanza_value_error(repo,servicio):
    repo.guardar(servicio)
    caso_uso=IniciarServicio(repo)

    with pytest.raises(ValueError):
        caso_uso.ejecutar(servicio.id)



