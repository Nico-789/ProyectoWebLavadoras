from domain.enum.estadosolicitud import EstadoSolicitud
from domain.entities.solicitud import Solicitud
import pytest
from datetime import date, time


@pytest.fixture
def solicitud():
    solicitud = Solicitud(
        id=1,
        id_electrodomestico=1,
        id_tipo_servicio=1,
        problema="No centrifuga",
        fecha_solicitada=date.today(),
        hora_solicitada=time(10, 0),
        fecha=date.today(),
        hora_inicial=time(8, 0),
        hora_final=time(9, 0),
    )
    return solicitud


def test_solicitud_se_crea_como_enviada(solicitud):
    assert solicitud.estado == EstadoSolicitud.ENVIADA


def test_solicitud_poner_en_revision(solicitud):
    solicitud.poner_en_revision()
    assert solicitud.estado == EstadoSolicitud.EN_REVISION


def test_solicitud_rechazar(solicitud):
    solicitud.poner_en_revision()
    solicitud.rechazar()
    assert solicitud.estado == EstadoSolicitud.RECHAZADA


def test_solicitud_convertir_en_servicio(solicitud):
    solicitud.poner_en_revision()
    solicitud.convertir_en_servicio()
    assert solicitud.estado == EstadoSolicitud.CONVERTIDA_EN_SERVICIO


@pytest.mark.parametrize(
    "pasos_previos, accion_invalida",
    [
        pytest.param(
            [],
            "convertir_en_servicio",
            id="no_se_puede_convertir_una_solicitud_enviada",
        ),
        pytest.param(
            ["poner_en_revision", "rechazar"],
            "rechazar",
            id="rechazar_dos_veces_lanza_error",
        ),
        pytest.param(
            ["poner_en_revision", "rechazar"],
            "convertir_en_servicio",
            id="no_se_puede_convertir_una_solicitud_ya_rechazada",
        ),
    ],
)
def test_transiciones_invalidas_lanzan_value_error(solicitud, pasos_previos, accion_invalida):
    for paso in pasos_previos:
        getattr(solicitud, paso)()

    with pytest.raises(ValueError):
        getattr(solicitud, accion_invalida)()

def test_convertir_en_servicio_retorna_self(solicitud):
    solicitud.poner_en_revision()
    resutado=solicitud.convertir_en_servicio()
    assert resutado is not None
    assert resutado is solicitud

