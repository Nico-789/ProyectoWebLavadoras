import os
import pytest
import pyodbc
from datetime import datetime
from dotenv import load_dotenv
from domain.entities.servicio import Servicio
from domain.enum.estadoservicio import estadoServicio
from infrastructure.repositories.sql_server_servicio_repository import SqlServerServicioRepository

load_dotenv()
CONNECTION_STRING = os.getenv("TEST_DB_CONNECTION_STRING")


def crear_servicio(id=None, problema="Fuga de agua", estado=estadoServicio.PENDIENTE,
    fecha_hora_inicio=datetime(2026, 11, 3, 9, 0)):
    return Servicio(
        id=id,
        id_electrodomestico=1,
        id_tipo_servicio=1,
        problema=problema,
        fecha_hora_inicio=fecha_hora_inicio,
        estado=estado,
    )


@pytest.fixture
def repo():
    with pyodbc.connect(CONNECTION_STRING) as conexion:
        conexion.execute("DELETE FROM Servicio")
    return SqlServerServicioRepository(CONNECTION_STRING)


def test_guardar_asigna_id_y_obtener_por_id_lo_recupera(repo):
    servicio = crear_servicio()

    repo.guardar(servicio)
    encontrado = repo.obtener_por_id(servicio.id)

    assert servicio.id is not None
    assert encontrado is not None
    assert encontrado.problema == "Fuga de agua"
    assert encontrado.estado == estadoServicio.PENDIENTE
    assert encontrado.fecha_hora_fin == datetime(2026, 11, 3, 10, 0)

def test_guardar_actualiza_el_servicio_si_ya_tiene_id(repo):
    servicio = crear_servicio()
    repo.guardar(servicio)
    servicio.marcar_proximo_a_iniciar()
    servicio.iniciar()
    repo.guardar(servicio)

    encontrado = repo.obtener_por_id(servicio.id)

    assert encontrado.estado == estadoServicio.EN_CURSO
    assert encontrado.fecha_hora_inicio_real is not None

def test_listar_por_estado_devuelve_solo_los_servicios_de_ese_estado(repo):
    pendiente = crear_servicio(problema="Fuga de agua", estado=estadoServicio.PENDIENTE)
    finalizado = crear_servicio(problema="No enciende", estado=estadoServicio.FINALIZADO)
    repo.guardar(pendiente)
    repo.guardar(finalizado)

    resultado = repo.listar_por_estado(estadoServicio.FINALIZADO)

    assert len(resultado) == 1
    assert resultado[0].problema == "No enciende"

def test_listar_todos_devuelve_los_servicios_ordenados_por_fecha_hora_inicio(repo):
    tarde = crear_servicio(problema="Fuga de agua", fecha_hora_inicio=datetime(2026, 11, 3, 15, 0))
    temprano = crear_servicio(problema="No enciende", fecha_hora_inicio=datetime(2026, 11, 3, 9, 0))
    repo.guardar(tarde)
    repo.guardar(temprano)

    resultado = repo.listar_todos()

    assert len(resultado) == 2
    assert resultado[0].problema == "No enciende"
    assert resultado[1].problema == "Fuga de agua"

def test_listar_por_rango_devuelve_solo_los_servicios_dentro_del_rango(repo):
    dentro = crear_servicio(problema="Dentro", fecha_hora_inicio=datetime(2026, 11, 3, 10, 0))
    mismo_dia_tarde = crear_servicio(problema="Tarde", fecha_hora_inicio=datetime(2026, 11, 3, 15, 0))
    otro_dia = crear_servicio(problema="Otro dia", fecha_hora_inicio=datetime(2026, 11, 4, 10, 0))
    repo.guardar(dentro)
    repo.guardar(mismo_dia_tarde)
    repo.guardar(otro_dia)

    resultado = repo.listar_por_rango(datetime(2026, 11, 3, 9, 0), datetime(2026, 11, 3, 12, 0))

    assert len(resultado) == 1
    assert resultado[0].problema == "Dentro"

def test_eliminar_borra_la_solicitud_y_devuelve_true(repo):
    servicio = crear_servicio()
    repo.guardar(servicio)

    resultado = repo.eliminar(servicio.id)

    assert resultado is True
    assert repo.obtener_por_id(servicio.id) is None

def test_eliminar_devuelve_false_si_el_id_no_existe(repo):
    resultado = repo.eliminar(99999)

    assert resultado is False