"""Clase abstracta Servicio y tres servicios especializados (polimorfismo)."""

from abc import ABC, abstractmethod

from entidad import EntidadBase
from excepciones import (
    CalculoInconsistenteError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
)


class Servicio(EntidadBase, ABC):
    """Servicio genérico de Software FJ."""

    IVA = 0.19  # Impuesto de referencia para el cálculo con IVA.

    def __init__(self, nombre, tarifa_base, disponible=True):
        super().__init__()
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError("El nombre del servicio no puede estar vacío.")
        try:
            tarifa = float(tarifa_base)  # Acepta números o texto numérico.
        except (TypeError, ValueError) as error:
            raise ServicioInvalidoError(f"Tarifa no numérica: {tarifa_base!r}") from error
        if tarifa <= 0:
            raise ServicioInvalidoError("La tarifa base debe ser mayor que cero.")
        self._nombre = nombre.strip()  # Atributos protegidos (encapsulación).
        self._tarifa_base = tarifa
        self._disponible = bool(disponible)

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool):
        self._disponible = bool(valor)

    # ---------- métodos que cada servicio sobrescribe ----------
    @abstractmethod
    def validar_parametros(self, duracion) -> None:
        """Valida la duración y los parámetros propios del servicio."""

    @abstractmethod
    def calcular_costo_base(self, duracion) -> float:
        """Costo sin descuentos ni impuestos."""

    @abstractmethod
    def describir(self) -> str:
        """Descripción del servicio."""

    # ---------- utilidades compartidas ----------
    def _verificar_disponibilidad(self):
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self._nombre}' no está disponible.")

    @staticmethod
    def _validar_rango(duracion, minimo, maximo, unidad):
        """Comprueba que la duración sea numérica y esté en el rango permitido."""
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):
            raise ServicioInvalidoError(f"La duración debe ser numérica, se recibió {duracion!r}.")
        if not minimo <= duracion <= maximo:
            raise ServicioInvalidoError(f"Duración fuera de rango: {minimo}-{maximo} {unidad}.")

    # ---------- método sobrecargado (parámetros opcionales) ----------
    def calcular_costo(self, duracion, descuento=None, impuesto=None) -> float:
        """Sobrecarga simulada con parámetros opcionales:
        calcular_costo(d)                  -> costo base
        calcular_costo(d, 0.10)            -> con descuento
        calcular_costo(d, impuesto=0.19)   -> con impuesto
        calcular_costo(d, 0.10, 0.19)      -> con descuento e impuesto
        """
        self.validar_parametros(duracion)  # Valida antes de calcular.
        costo = self.calcular_costo_base(duracion)
        if descuento is not None:
            if not isinstance(descuento, (int, float)) or not 0 <= descuento < 1:
                raise CalculoInconsistenteError(f"Descuento inconsistente: {descuento!r} (debe estar en [0, 1)).")
            costo *= 1 - descuento
        if impuesto is not None:
            if not isinstance(impuesto, (int, float)) or impuesto < 0:
                raise CalculoInconsistenteError(f"Impuesto inconsistente: {impuesto!r}.")
            costo *= 1 + impuesto
        return round(costo, 2)

    def calcular_costo_con_iva(self, duracion) -> float:
        """Variante de cálculo que aplica el IVA por defecto."""
        return self.calcular_costo(duracion, impuesto=self.IVA)


class ReservaSala(Servicio):
    """Reserva de salas (se cobra por hora)."""

    def __init__(self, nombre, tarifa_por_hora, capacidad, disponible=True):
        super().__init__(nombre, tarifa_por_hora, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError("La capacidad de la sala debe ser un entero positivo.")
        self._capacidad = capacidad

    def validar_parametros(self, horas) -> None:
        self._verificar_disponibilidad()
        self._validar_rango(horas, 1, 8, "horas")

    def calcular_costo_base(self, horas) -> float:
        return self._tarifa_base * horas

    def describir(self) -> str:
        return f"Sala '{self._nombre}' | Capacidad: {self._capacidad} personas | ${self._tarifa_base:,.0f}/hora"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos (se cobra por día y por unidad)."""

    def __init__(self, nombre, tarifa_por_dia, equipo, cantidad=1, disponible=True):
        super().__init__(nombre, tarifa_por_dia, disponible)
        if not isinstance(equipo, str) or not equipo.strip():
            raise ServicioInvalidoError("Debe indicar el tipo de equipo.")
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ServicioInvalidoError("La cantidad de equipos debe ser un entero positivo.")
        self._equipo = equipo.strip()
        self._cantidad = cantidad

    def validar_parametros(self, dias) -> None:
        self._verificar_disponibilidad()
        self._validar_rango(dias, 1, 30, "días")

    def calcular_costo_base(self, dias) -> float:
        costo = self._tarifa_base * dias * self._cantidad
        if dias >= 7:  # Descuento por alquiler semanal.
            costo *= 0.90
        return costo

    def describir(self) -> str:
        return f"Alquiler de {self._cantidad} x {self._equipo} | ${self._tarifa_base:,.0f}/día"


class AsesoriaEspecializada(Servicio):
    """Asesorías especializadas (por hora, con recargo según el nivel)."""

    RECARGOS = {"junior": 1.0, "senior": 1.5, "experto": 2.0}  # Multiplicador por nivel.

    def __init__(self, nombre, tarifa_por_hora, especialidad, nivel="junior", disponible=True):
        super().__init__(nombre, tarifa_por_hora, disponible)
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ServicioInvalidoError("Debe indicar la especialidad de la asesoría.")
        if nivel not in self.RECARGOS:
            raise ServicioInvalidoError(f"Nivel inválido: {nivel!r}. Opciones: {', '.join(self.RECARGOS)}.")
        self._especialidad = especialidad.strip()
        self._nivel = nivel

    def validar_parametros(self, horas) -> None:
        self._verificar_disponibilidad()
        self._validar_rango(horas, 0.5, 4, "horas")

    def calcular_costo_base(self, horas) -> float:
        return self._tarifa_base * horas * self.RECARGOS[self._nivel]

    def describir(self) -> str:
        return f"Asesoría de {self._especialidad} (nivel {self._nivel}) | ${self._tarifa_base:,.0f}/hora base"
