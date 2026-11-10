from datetime import datetime

import pyodbc

from domain.entities.servicio import Servicio
from domain.enum.estadoservicio import estadoServicio
from domain.repositories.servicio_repository import ServicioRepository


class SqlServerServicioRepository(ServicioRepository):
    def __init__(self, connection_string: str):
        self._connection_string = connection_string

    def _fila_a_servicio(self, fila):
        servicio = Servicio(
            id=fila.id,
            id_electrodomestico=fila.id_electrodomestico,
            id_tipo_servicio=fila.id_tipo_servicio,
            problema=fila.problema,
            fecha_hora_inicio=fila.fecha_hora_inicio,
            estado=estadoServicio[fila.estado],
        )
        servicio.duracion_estimada = fila.duracion_estimada
        servicio.fecha_hora_fin = fila.fecha_hora_fin
        servicio.fecha_hora_inicio_real =fila.fecha_hora_inicio_real
        servicio.fecha_hora_fin_real = fila.fecha_hora_fin_real
        servicio.duracion_real = fila.duracion_real
        return servicio

    def guardar(self, servicio):
        conexion = pyodbc.connect(self._connection_string)
        try:
            if servicio.id is None:
                cursor = conexion.execute(
                    "INSERT INTO Servicio (id_electrodomestico, id_tipo_servicio, problema, "
                    "fecha_hora_inicio, fecha_hora_fin, duracion_estimada, "
                    "fecha_hora_inicio_real, fecha_hora_fin_real, duracion_real, estado) "
                    "OUTPUT INSERTED.id "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        servicio.id_electrodomestico,
                        servicio.id_tipo_servicio,
                        servicio.problema,
                        servicio.fecha_hora_inicio,
                        servicio.fecha_hora_fin,
                        servicio.duracion_estimada,
                        servicio.fecha_hora_inicio_real,
                        servicio.fecha_hora_fin_real,
                        servicio.duracion_real,
                        servicio.estado.name,
                    ),
                )
                servicio.id = cursor.fetchone()[0]
            else:
                conexion.execute(
                    "UPDATE Servicio SET id_electrodomestico = ?, id_tipo_servicio = ?, "
                    "problema = ?, fecha_hora_inicio = ?, fecha_hora_fin = ?, "
                    "duracion_estimada = ?, fecha_hora_inicio_real = ?, "
                    "fecha_hora_fin_real = ?, duracion_real = ?, estado = ? "
                    "WHERE id = ?",
                    (
                        servicio.id_electrodomestico,
                        servicio.id_tipo_servicio,
                        servicio.problema,
                        servicio.fecha_hora_inicio,
                        servicio.fecha_hora_fin,
                        servicio.duracion_estimada,
                        servicio.fecha_hora_inicio_real,
                        servicio.fecha_hora_fin_real,
                        servicio.duracion_real,
                        servicio.estado.name,
                        servicio.id,
                    ),
                )
            conexion.commit()
        finally:
            conexion.close()

    def obtener_por_id(self, id):
        with pyodbc.connect(self._connection_string) as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT id, id_electrodomestico, id_tipo_servicio, problema, "
                "fecha_hora_inicio, duracion_estimada, fecha_hora_fin, fecha_hora_inicio_real, fecha_hora_fin_real, duracion_real, estado "
                "FROM Servicio WHERE id = ?",
                (id,),
            )
            fila = cursor.fetchone()
            if fila is None:
                return None
            return self._fila_a_servicio(fila)

    def listar_todos(self):
        with pyodbc.connect(self._connection_string) as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT id, id_electrodomestico, id_tipo_servicio, problema, "
                "fecha_hora_inicio, fecha_hora_fin, duracion_estimada, "
                "fecha_hora_inicio_real, fecha_hora_fin_real, duracion_real, estado "
                "FROM Servicio ORDER BY fecha_hora_inicio"
            )
            filas = cursor.fetchall()
            return [self._fila_a_servicio(fila) for fila in filas]

    def listar_por_estado(self, estado):
        with pyodbc.connect(self._connection_string) as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT id, id_electrodomestico, id_tipo_servicio, problema, "
                "fecha_hora_inicio, fecha_hora_fin, duracion_estimada, "
                "fecha_hora_inicio_real, fecha_hora_fin_real, duracion_real, estado "
                "FROM Servicio WHERE estado = ?",
                (estado.name,),
            )
            filas = cursor.fetchall()
            return [self._fila_a_servicio(fila) for fila in filas]

    def listar_por_rango(self, fecha_hora_inicio, fecha_hora_fin):
        with pyodbc.connect(self._connection_string) as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT id, id_electrodomestico, id_tipo_servicio, problema, "
                "fecha_hora_inicio, fecha_hora_fin, duracion_estimada, "
                "fecha_hora_inicio_real, fecha_hora_fin_real, duracion_real, estado "
                "FROM Servicio WHERE fecha_hora_inicio >= ? AND fecha_hora_inicio <= ? "
                "ORDER BY fecha_hora_inicio",
                (fecha_hora_inicio, fecha_hora_fin),
            )
            filas = cursor.fetchall()
            return [self._fila_a_servicio(fila) for fila in filas]

    def eliminar(self, id):
        conexion = pyodbc.connect(self._connection_string)
        try:
            cursor = conexion.cursor()
            cursor.execute(
                "DELETE FROM Servicio WHERE id = ?",
                (id,),
            )
            conexion.commit()
            return cursor.rowcount > 0
        finally:
            conexion.close()