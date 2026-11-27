"""Clase abstracta que representa las entidades generales del sistema."""

from abc import ABC, abstractmethod  # Herramientas para crear clases abstractas
from itertools import count  # Generador de números consecutivos


class EntidadBase(ABC):  # Clase abstracta: no se puede instanciar directamente
    """Base abstracta de Cliente, Servicio y Reserva."""

    _contador = count(1)  # Generador compartido de identificadores únicos (1, 2, 3, ...)

    def __init__(self):  # Constructor de la entidad
        self._id = next(EntidadBase._contador)  # Asigna el siguiente id (atributo protegido: encapsulación)

    @property  # Permite leer el id como si fuera un atributo
    def id(self) -> int:  # Propiedad de solo lectura
        """Identificador de solo lectura."""
        return self._id  # Devuelve el identificador

    @abstractmethod  # Obliga a las clases hijas a implementar este método
    def describir(self) -> str:  # Método abstracto: cada entidad se describe a sí misma
        """Cada entidad debe describirse a sí misma (polimorfismo)."""

    def __str__(self) -> str:  # Se ejecuta al usar print(objeto) o str(objeto)
        return self.describir()  # Usa la descripción propia de cada clase hija
