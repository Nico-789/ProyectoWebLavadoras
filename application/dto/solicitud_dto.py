from datetime import date, time
from dataclasses import dataclass

@dataclass
class SolicitudDTO:
      id: int
      id_electrodomestico: int
      id_tipo_servicio: int
      problema:str
      fecha_solicitada: date 
      hora_solicitada: time 
      fecha: date
      hora_inicial:time
      hora_final:time
      

