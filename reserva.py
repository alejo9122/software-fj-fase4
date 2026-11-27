"""Clase Reserva: integra cliente, servicio, duración y estado."""

from enum import Enum

from cliente import Cliente
from entidad import EntidadBase
from excepciones import (
    CalculoInconsistenteError,
    OperacionNoPermitidaError,
    ParametroFaltanteError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
    SoftwareFJError,
)
from logger_config import obtener_logger
from servicios import Servicio

logger = obtener_logger()


class EstadoReserva(Enum):
    """Estados posibles de una reserva."""

    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
    PROCESADA = "Procesada"


class Reserva(EntidadBase):
    """Reserva de un servicio por parte de un cliente."""

    def __init__(self, cliente=None, servicio=None, duracion=None):
        super().__init__()
        if cliente is None or servicio is None or duracion is None:
            raise ParametroFaltanteError("Una reserva requiere cliente, servicio y duración.")
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("El cliente de la reserva no es un objeto Cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("El servicio de la reserva no es un objeto Servicio válido.")
        try:
            servicio.validar_parametros(duracion)  # Valida disponibilidad y duración.
        except SoftwareFJError as error:
            # Encadenamiento: la causa original (error del servicio) queda registrada.
            raise ReservaInvalidaError(f"No se puede crear la reserva: {error}") from error
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = EstadoReserva.PENDIENTE
        self._costo_total = None  # Se calcula al procesar.

    @property
    def estado(self) -> EstadoReserva:
        return self._estado

    @property
    def costo_total(self):
        return self._costo_total

    def confirmar(self) -> None:
        """Pendiente -> Confirmada (try/except/else/finally)."""
        if self._estado != EstadoReserva.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"Solo se puede confirmar una reserva pendiente (estado actual: {self._estado.value})."
            )
        try:
            self._servicio.validar_parametros(self._duracion)  # Revalida disponibilidad.
        except ServicioNoDisponibleError as error:
            raise ReservaInvalidaError("El servicio dejó de estar disponible.") from error
        else:
            self._estado = EstadoReserva.CONFIRMADA  # Solo si no hubo error.
            logger.info("Reserva #%s confirmada.", self.id)
        finally:
            logger.debug("Fin del intento de confirmar la reserva #%s.", self.id)

    def cancelar(self) -> None:
        """Pendiente/Confirmada -> Cancelada."""
        if self._estado in (EstadoReserva.CANCELADA, EstadoReserva.PROCESADA):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar una reserva {self._estado.value.lower()}."
            )
        self._estado = EstadoReserva.CANCELADA
        logger.info("Reserva #%s cancelada.", self.id)

    def procesar(self, descuento=None, impuesto=None) -> float:
        """Confirmada -> Procesada. Calcula y devuelve el costo total."""
        if self._estado != EstadoReserva.CONFIRMADA:
            raise OperacionNoPermitidaError(
                f"Solo se procesa una reserva confirmada (estado actual: {self._estado.value})."
            )
        try:
            costo = self._servicio.calcular_costo(self._duracion, descuento, impuesto)
            if costo <= 0:
                raise CalculoInconsistenteError(f"Costo no válido calculado: {costo}.")
        except SoftwareFJError as error:
            logger.error("Fallo al procesar la reserva #%s: %s", self.id, error)
            raise ReservaInvalidaError(f"No se pudo procesar la reserva #{self.id}.") from error
        else:
            self._estado = EstadoReserva.PROCESADA
            self._costo_total = costo
            logger.info("Reserva #%s procesada. Costo total: %.2f", self.id, costo)
            return costo
        finally:
            logger.debug("Fin del intento de procesar la reserva #%s.", self.id)

    def describir(self) -> str:
        costo = f" | Total: ${self._costo_total:,.2f}" if self._costo_total is not None else ""
        return (
            f"Reserva #{self.id} [{self._estado.value}] | {self._cliente.nombre} -> "
            f"{self._servicio.nombre} x {self._duracion}{costo}"
        )
