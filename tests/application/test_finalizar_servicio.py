from domain.enum.estadoservicio import estadoServicio
from domain.entities.servicio import Servicio
import pytest
from infrastructure.repositories.in_memory_servicio_repository import InMemoryServicioRepository
from datetime import datetime
from application.use_cases.finalizar_servicio import FinalizarServicio
from application.exceptions import ServicioNoEncontrado

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

def test_finalizar_servicio_cambia_el_estado_a_finalizado(repo, servicio):
    servicio.marcar_proximo_a_iniciar()
    servicio.iniciar()
    repo.guardar(servicio)
    caso_uso=FinalizarServicio(repo)
    caso_uso.ejecutar(servicio.id)
    encontrada = repo.obtener_por_id(servicio.id)

    assert encontrada is not None
    assert encontrada.duracion_real is not None
    assert encontrada.estado == estadoServicio.FINALIZADO

def test_finalizar_servicio_sin_estar_en_curso_lanza_value_error(repo, servicio):
    repo.guardar(servicio)
    caso_uso=FinalizarServicio(repo)
    
    with pytest.raises(ValueError):
        caso_uso.ejecutar(servicio.id)

def test_finalizar_servicio_inexistente_lanza_error(repo):
    caso_uso = FinalizarServicio(repo)

    with pytest.raises(ServicioNoEncontrado):
        caso_uso.ejecutar(99999)