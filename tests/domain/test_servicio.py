from domain.enum.estadoservicio import estadoServicio
from domain.entities.servicio import Servicio
from unittest.mock import patch
import pytest
from datetime import datetime

#PRUEBAS UNITARIAS
@pytest.fixture
def servicio():
    fecha_inicio = datetime(2026, 8, 17, 10, 30)

    servicio = Servicio(
        id=1,
        id_electrodomestico=5,
        id_tipo_servicio=1,
        problema="No centrifuga",
        fecha_hora_inicio=fecha_inicio
    )

    return servicio

def test_servicio_se_crea_como_pendiente(servicio):
    assert servicio.estado == estadoServicio.PENDIENTE

def test_marcar_proximo_a_iniciar(servicio):
    servicio.marcar_proximo_a_iniciar()
    assert servicio.estado == estadoServicio.PROXIMO_A_INICIAR

def test_iniciar_servicio(servicio):
    servicio.marcar_proximo_a_iniciar()
    servicio.iniciar()

    assert servicio.estado == estadoServicio.EN_CURSO
    assert servicio.fecha_hora_inicio_real is not None

def test_finalizar_servicio(servicio):
    servicio.marcar_proximo_a_iniciar()
    servicio.iniciar()
    servicio.finalizar()

    assert servicio.estado == estadoServicio.FINALIZADO
    assert servicio.fecha_hora_inicio_real is not None
    assert servicio.fecha_hora_fin_real is not None
    assert servicio.duracion_real is not None

@pytest.mark.parametrize(
    "pasos_previos, accion_invalida",
    [
        pytest.param([], "iniciar", id="no_se_puede_iniciar_un_servicio_pendiente"),
        pytest.param([], "finalizar", id="no_se_puede_finalizar_un_servicio_pendiente"),
        pytest.param(["marcar_proximo_a_iniciar"], "finalizar", id="no_se_puede_finalizar_un_servicio_proximo_a_iniciar"),
        pytest.param(["marcar_proximo_a_iniciar", "iniciar"], "iniciar", id="intentar_iniciar_un_servicio_dos_veces"),
        pytest.param(["marcar_proximo_a_iniciar", "iniciar", "finalizar"], "finalizar", id="intentar_finalizar_un_servicio_dos_veces"),
    ],
)
def test_transiciones_invalidas_lanzan_value_error(servicio, pasos_previos, accion_invalida):
    for paso in pasos_previos:
        getattr(servicio, paso)()

    with pytest.raises(ValueError):
        getattr(servicio, accion_invalida)()

def test_duracion_real_se_calcula_al_finalizar(servicio):

    with patch("domain.entities.servicio.datetime") as mock_datetime:

        mock_datetime.now.side_effect = [
            datetime(2026, 8, 17, 10, 30),
            datetime(2026, 8, 17, 11, 0)
        ]

        servicio.marcar_proximo_a_iniciar()
        servicio.iniciar()
        servicio.finalizar()

        assert servicio.duracion_real == 30