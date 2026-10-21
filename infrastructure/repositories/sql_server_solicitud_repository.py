import pyodbc
from domain.repositories.solicitud_repository import SolicitudRepository
from domain.entities.solicitud import Solicitud
from domain.enum.estadosolicitud import EstadoSolicitud


class SqlServerSolicitudRepository(SolicitudRepository):
    def __init__(self, connection_string: str):
        self._connection_string = connection_string

    def obtener_por_id(self, id: int) -> Solicitud | None:
        with pyodbc.connect(self._connection_string) as conexion:
            fila = conexion.execute(
                "SELECT id, id_electrodomestico, id_tipo_servicio, problema, "
                "fecha_solicitada, hora_solicitada, fecha, hora_inicial, hora_final, estado "
                "FROM Solicitud WHERE id = ?",
                (id,),
            ).fetchone()

        if fila is None:
            return None

        return Solicitud(
            id=fila.id,
            id_electrodomestico=fila.id_electrodomestico,
            id_tipo_servicio=fila.id_tipo_servicio,
            problema=fila.problema,
            fecha_solicitada=fila.fecha_solicitada,
            hora_solicitada=fila.hora_solicitada,
            fecha=fila.fecha,
            hora_inicial=fila.hora_inicial,
            hora_final=fila.hora_final,
            estado=EstadoSolicitud[fila.estado],
        )

    def guardar(self, solicitud: Solicitud) -> None:
        conexion = pyodbc.connect(self._connection_string)
        try:
            if solicitud.id is None:
                cursor = conexion.execute(
                    "INSERT INTO Solicitud (id_electrodomestico, id_tipo_servicio, problema, "
                    "fecha_solicitada, hora_solicitada, fecha, hora_inicial, hora_final, estado) "
                    "OUTPUT INSERTED.id "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        solicitud.id_electrodomestico,
                        solicitud.id_tipo_servicio,
                        solicitud.problema,
                        solicitud.fecha_solicitada,
                        solicitud.hora_solicitada,
                        solicitud.fecha,
                        solicitud.hora_inicial,
                        solicitud.hora_final,
                        solicitud.estado.name,
                    ),
                )
                solicitud.id = cursor.fetchone()[0]
            else:
                conexion.execute(
                    "UPDATE Solicitud SET id_electrodomestico=?, id_tipo_servicio=?, problema=?, fecha_solicitada=?, hora_solicitada=?, fecha=?, hora_inicial=?, hora_final=?, estado=? WHERE id = ?",
                    (
                        solicitud.id_electrodomestico,
                        solicitud.id_tipo_servicio,
                        solicitud.problema,
                        solicitud.fecha_solicitada,
                        solicitud.hora_solicitada,
                        solicitud.fecha,
                        solicitud.hora_inicial,
                        solicitud.hora_final,
                        solicitud.estado.name,
                        solicitud.id,
                    ),
                )
            conexion.commit()
        finally:
            conexion.close()

    def listar_por_estado(self, estado: EstadoSolicitud) -> list[Solicitud]:
        raise NotImplementedError

    def listar_todas(self) -> list[Solicitud]:
        raise NotImplementedError

    def eliminar(self, id: int) -> bool:
        raise NotImplementedError            