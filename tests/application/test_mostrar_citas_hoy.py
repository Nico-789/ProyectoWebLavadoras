from datetime import date, datetime, time, timedelta
from application.use_cases.mostrar_citas_hoy import MostrarCitasHoy
from domain.repositories.servicio_repository import ServicioRepository
from infrastructure.repositories.in_memory_servicio_repository import InMemoryServicioRepository
from domain.enum.estadoservicio import estadoServicio
from domain.entities.servicio import Servicio
import pytest

def crear_servicio(id=1, problema="No centrifuga", estado=estadoServicio.PENDIENTE,fecha_hora_inicio=datetime.combine(date.today(), time(10, 0))):
    return Servicio(
        id=id,
        id_electrodomestico=1,
        id_tipo_servicio=1,
        problema=problema,
        fecha_hora_inicio=fecha_hora_inicio,
        estado=estado,
    )   

@pytest.fixture
def servicio():
    return crear_servicio()

@pytest.fixture
def repo():
    return InMemoryServicioRepository()

def test_mostrar_citas_hoy_incluye_el_servicio_de_hoy(repo,servicio):
    repo.guardar(servicio)
    caso_uso=MostrarCitasHoy(repo)
    resultado=caso_uso.ejecutar()

    assert len(resultado) == 1
    assert resultado[0].id == servicio.id

def test_mostrar_citas_hoy_no_incluye_servicios_de_otro_dia(repo):
    ayer = date.today()-timedelta(days=1)
    servicio_ayer = crear_servicio(id=2, fecha_hora_inicio=datetime.combine(ayer, time(10, 0)))
    repo.guardar(servicio_ayer)
    caso_uso = MostrarCitasHoy(repo)
    resultado = caso_uso.ejecutar()


    assert resultado == []