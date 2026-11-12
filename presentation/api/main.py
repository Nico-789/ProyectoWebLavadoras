import os
from datetime import date, datetime, time
from fastapi import Depends, FastAPI, HTTPException

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from application.dto.solicitud_dto import SolicitudDTO
from application.use_cases.crear_solicitud import CrearSolicitud
from application.use_cases.listar_solicitudes import ListarSolicitudes
from infrastructure.repositories.sql_server_solicitud_repository import SqlServerSolicitudRepository
from application.exceptions import SolicitudNoEncontrada
from application.use_cases.rechazar_solicitud import RechazarSolicitud
from application.use_cases.convertir_solicitud_en_servicio import ConvertirSolicitudEnServicio
from infrastructure.repositories.sql_server_servicio_repository import SqlServerServicioRepository
from application.exceptions import ServicioNoEncontrado
from application.use_cases.finalizar_servicio import FinalizarServicio
from application.use_cases.iniciar_servicio import IniciarServicio
from application.use_cases.marcar_servicio_proximo_a_iniciar import MarcarServicioProximoAIniciar
from application.use_cases.mostrar_citas_hoy import MostrarCitasHoy

load_dotenv()

app = FastAPI(title="Lavadoras API")


class SolicitudRespuesta(BaseModel):
    id: int
    id_electrodomestico: int
    id_tipo_servicio: int
    problema: str
    fecha_solicitada: date
    hora_solicitada: time
    fecha: date
    hora_inicial: time
    hora_final: time
    estado: str

class ServicioRespuesta(BaseModel):
    id: int
    id_electrodomestico: int
    id_tipo_servicio: int
    problema: str
    fecha_hora_inicio: datetime
    fecha_hora_fin: datetime
    duracion_estimada: int
    fecha_hora_inicio_real: datetime | None
    fecha_hora_fin_real: datetime | None
    duracion_real: int | None
    estado: str


def obtener_repo_servicios():
    return SqlServerServicioRepository(os.getenv("DB_CONNECTION_STRING"))


def a_respuesta_servicio(s):
    return ServicioRespuesta(
        id=s.id,
        id_electrodomestico=s.id_electrodomestico,
        id_tipo_servicio=s.id_tipo_servicio,
        problema=s.problema,
        fecha_hora_inicio=s.fecha_hora_inicio,
        fecha_hora_fin=s.fecha_hora_fin,
        duracion_estimada=s.duracion_estimada,
        fecha_hora_inicio_real=s.fecha_hora_inicio_real,
        fecha_hora_fin_real=s.fecha_hora_fin_real,
        duracion_real=s.duracion_real,
        estado=s.estado.name,
    )

class SolicitudEntrada(BaseModel):
    id_electrodomestico: int
    id_tipo_servicio: int
    problema: str
    fecha: date
    hora_inicial: time
    hora_final: time


def obtener_repo_solicitudes():
    return SqlServerSolicitudRepository(os.getenv("DB_CONNECTION_STRING"))


def a_respuesta(s):
    return SolicitudRespuesta(
        id=s.id,
        id_electrodomestico=s.id_electrodomestico,
        id_tipo_servicio=s.id_tipo_servicio,
        problema=s.problema,
        fecha_solicitada=s.fecha_solicitada,
        hora_solicitada=s.hora_solicitada,
        fecha=s.fecha,
        hora_inicial=s.hora_inicial,
        hora_final=s.hora_final,
        estado=s.estado.name,
    )


@app.get("/health")
def estado():
    return {"estado": "ok"}


@app.get("/solicitudes", response_model=list[SolicitudRespuesta])
def listar_solicitudes(repo=Depends(obtener_repo_solicitudes)):
    solicitudes = ListarSolicitudes(repo).ejecutar()
    return [a_respuesta(s) for s in solicitudes]



@app.post("/solicitudes", response_model=SolicitudRespuesta, status_code=201)
def crear_solicitud(entrada: SolicitudEntrada, repo=Depends(obtener_repo_solicitudes)):
    ahora = datetime.now()
    dto = SolicitudDTO(
        id=None,
        id_electrodomestico=entrada.id_electrodomestico,
        id_tipo_servicio=entrada.id_tipo_servicio,
        problema=entrada.problema,
        fecha_solicitada=ahora.date(),
        hora_solicitada=ahora.time(),
        fecha=entrada.fecha,
        hora_inicial=entrada.hora_inicial,
        hora_final=entrada.hora_final,
    )
    solicitud = CrearSolicitud(repo).ejecutar(dto)
    return a_respuesta(solicitud)

@app.post("/solicitudes/{solicitud_id}/rechazar", response_model=SolicitudRespuesta)
def rechazar_solicitud(solicitud_id: int, repo=Depends(obtener_repo_solicitudes)):
    try:
        solicitud = RechazarSolicitud(repo).ejecutar(solicitud_id)
    except SolicitudNoEncontrada:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))
    return a_respuesta(solicitud)

@app.post("/solicitudes/{solicitud_id}/convertir", response_model=ServicioRespuesta, status_code=201)
def convertir_solicitud(
    solicitud_id: int,
    repo_solicitudes=Depends(obtener_repo_solicitudes),
    repo_servicios=Depends(obtener_repo_servicios),
):
    try:
        servicio = ConvertirSolicitudEnServicio(repo_solicitudes, repo_servicios).ejecutar(solicitud_id)
    except SolicitudNoEncontrada:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))
    return a_respuesta_servicio(servicio)

def ejecutar_transicion(caso_uso, servicio_id):
    try:
        servicio = caso_uso.ejecutar(servicio_id)
    except ServicioNoEncontrado:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))
    return a_respuesta_servicio(servicio)


@app.post("/servicios/{servicio_id}/proximo-a-iniciar", response_model=ServicioRespuesta)
def marcar_servicio_proximo_a_iniciar(servicio_id: int, repo=Depends(obtener_repo_servicios)):
    return ejecutar_transicion(MarcarServicioProximoAIniciar(repo), servicio_id)


@app.post("/servicios/{servicio_id}/iniciar", response_model=ServicioRespuesta)
def iniciar_servicio(servicio_id: int, repo=Depends(obtener_repo_servicios)):
    return ejecutar_transicion(IniciarServicio(repo), servicio_id)


@app.post("/servicios/{servicio_id}/finalizar", response_model=ServicioRespuesta)
def finalizar_servicio(servicio_id: int, repo=Depends(obtener_repo_servicios)):
    return ejecutar_transicion(FinalizarServicio(repo), servicio_id)


@app.get("/servicios/hoy", response_model=list[ServicioRespuesta])
def mostrar_citas_hoy(repo=Depends(obtener_repo_servicios)):
    servicios = MostrarCitasHoy(repo).ejecutar()
    return [a_respuesta_servicio(s) for s in servicios]