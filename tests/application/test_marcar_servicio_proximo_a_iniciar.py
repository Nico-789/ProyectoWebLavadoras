from domain.enum.estadoservicio import estadoServicio
from domain.entities.servicio import Servicio
import pytest
from infrastructure.repositories.in_memory_servicio_repository import InMemoryServicioRepository
from datetime import datetime
from application.use_cases.marcar_servicio_proximo_a_iniciar import MarcarServicioProximoAIniciar
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

def test_marcar_servicio_proximo_a_iniciar_cambia_el_estado_a_proximo_a_iniciar(repo, servicio):
    repo.guardar(servicio)
    caso_uso = MarcarServicioProximoAIniciar(repo)
    caso_uso.ejecutar(servicio.id)
    encontrada = repo.obtener_por_id(servicio.id)

    assert encontrada is not None
    assert encontrada.estado == estadoServicio.PROXIMO_A_INICIAR

def test_marcar_servicio_proximo_a_iniciar_sin_estar_pendiente_lanza_value_error(repo,servicio):
    servicio.marcar_proximo_a_iniciar()
    repo.guardar(servicio)
    caso_uso=MarcarServicioProximoAIniciar(repo)
    
    with pytest.raises(ValueError):
        caso_uso.ejecutar(servicio.id)