"""Clase abstracta que representa las entidades generales del sistema."""

from abc import ABC, abstractmethod
from itertools import count


class EntidadBase(ABC):
    """Base abstracta de Cliente, Servicio y Reserva."""

    _contador = count(1)  # Generador compartido de identificadores únicos.

    def __init__(self):
        self._id = next(EntidadBase._contador)  # Atributo protegido (encapsulación).

    @property
    def id(self) -> int:
        """Identificador de solo lectura."""
        return self._id

    @abstractmethod
    def describir(self) -> str:
        """Cada entidad debe describirse a sí misma (polimorfismo)."""

    def __str__(self) -> str:
        return self.describir()  # str(objeto) usa la descripción propia.
