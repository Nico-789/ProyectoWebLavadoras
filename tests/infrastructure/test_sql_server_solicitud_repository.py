import os
import pytest
import pyodbc
from datetime import date, time
from dotenv import load_dotenv
from domain.entities.solicitud import Solicitud
from domain.enum.estadosolicitud import EstadoSolicitud
from infrastructure.repositories.sql_server_solicitud_repository import SqlServerSolicitudRepository

load_dotenv()
CONNECTION_STRING = os.getenv("TEST_DB_CONNECTION_STRING")


def crear_solicitud(id=None, problema="No centrifuga", estado=EstadoSolicitud.ENVIADA):
    return Solicitud(
        id=id,
        id_electrodomestico=1,
        id_tipo_servicio=1,
        problema=problema,
        fecha_solicitada=date.today(),
        hora_solicitada=time(10, 0),
        fecha=date.today(),
        hora_inicial=time(8, 0),
        hora_final=time(9, 0),
        estado=estado,
    )


@pytest.fixture
def repo():
    with pyodbc.connect(CONNECTION_STRING) as conexion:
        conexion.execute("DELETE FROM Solicitud")
    return SqlServerSolicitudRepository(CONNECTION_STRING)


def test_guardar_asigna_id_y_obtener_por_id_la_recupera(repo):
    solicitud = crear_solicitud()

    repo.guardar(solicitud)
    encontrada = repo.obtener_por_id(solicitud.id)

    assert solicitud.id is not None
    assert encontrada is not None
    assert encontrada.problema == "No centrifuga"
    assert encontrada.estado == EstadoSolicitud.ENVIADA