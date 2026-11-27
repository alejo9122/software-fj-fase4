"""Clase Reserva: integra cliente, servicio, duración y estado."""

from enum import Enum  # Para definir los estados de la reserva

from cliente import Cliente  # Clase Cliente (para validar el tipo)
from entidad import EntidadBase  # Clase base de las entidades
from excepciones import (  # Excepciones propias que usa la reserva
    CalculoInconsistenteError,  # Cálculo inconsistente
    OperacionNoPermitidaError,  # Operación no permitida en el estado actual
    ParametroFaltanteError,  # Falta un parámetro
    ReservaInvalidaError,  # Reserva inválida
    ServicioNoDisponibleError,  # Servicio no disponible
    SoftwareFJError,  # Excepción base del sistema
)  # Fin de la importación
from logger_config import obtener_logger  # Función que entrega el logger
from servicios import Servicio  # Clase abstracta Servicio (para validar el tipo)

logger = obtener_logger()  # Logger compartido para registrar eventos de la reserva


class EstadoReserva(Enum):  # Enumeración con los estados posibles
    """Estados posibles de una reserva."""

    PENDIENTE = "Pendiente"  # Reserva creada, aún sin confirmar
    CONFIRMADA = "Confirmada"  # Reserva confirmada
    CANCELADA = "Cancelada"  # Reserva cancelada
    PROCESADA = "Procesada"  # Reserva procesada y con costo calculado


class Reserva(EntidadBase):  # Reserva hereda de EntidadBase
    """Reserva de un servicio por parte de un cliente."""

    def __init__(self, cliente=None, servicio=None, duracion=None):  # Constructor de la reserva
        super().__init__()  # Obtiene el id desde la clase base
        if cliente is None or servicio is None or duracion is None:  # Si falta algún parámetro
            raise ParametroFaltanteError("Una reserva requiere cliente, servicio y duración.")  # Lanza el error
        if not isinstance(cliente, Cliente):  # El cliente debe ser un objeto Cliente
            raise ReservaInvalidaError("El cliente de la reserva no es un objeto Cliente válido.")  # Error
        if not isinstance(servicio, Servicio):  # El servicio debe ser un objeto Servicio
            raise ReservaInvalidaError("El servicio de la reserva no es un objeto Servicio válido.")  # Error
        try:  # Intenta validar disponibilidad y duración
            servicio.validar_parametros(duracion)  # Cada servicio valida a su manera (polimorfismo)
        except SoftwareFJError as error:  # Si el servicio reporta un error
            # Encadenamiento: la causa original (error del servicio) queda registrada.
            raise ReservaInvalidaError(f"No se puede crear la reserva: {error}") from error  # raise ... from error
        self._cliente = cliente  # Guarda el cliente
        self._servicio = servicio  # Guarda el servicio
        self._duracion = duracion  # Guarda la duración
        self._estado = EstadoReserva.PENDIENTE  # Toda reserva nueva inicia como pendiente
        self._costo_total = None  # El costo se calcula al procesar

    @property  # Getter del estado
    def estado(self) -> EstadoReserva:  # Permite leer reserva.estado
        return self._estado  # Devuelve el estado actual

    @property  # Getter del costo total
    def costo_total(self):  # Permite leer reserva.costo_total
        return self._costo_total  # Devuelve el costo (None si aún no se procesa)

    def confirmar(self) -> None:  # Pendiente -> Confirmada
        """Pendiente -> Confirmada (try/except/else/finally)."""
        if self._estado != EstadoReserva.PENDIENTE:  # Solo se confirma una reserva pendiente
            raise OperacionNoPermitidaError(  # Lanza el error de operación no permitida
                f"Solo se puede confirmar una reserva pendiente (estado actual: {self._estado.value})."  # Mensaje
            )  # Fin del raise
        try:  # Intenta revalidar el servicio
            self._servicio.validar_parametros(self._duracion)  # Revalida disponibilidad y duración
        except ServicioNoDisponibleError as error:  # Si el servicio dejó de estar disponible
            raise ReservaInvalidaError("El servicio dejó de estar disponible.") from error  # Excepción encadenada
        else:  # Se ejecuta solo si no hubo error
            self._estado = EstadoReserva.CONFIRMADA  # Cambia el estado a confirmada
            logger.info("Reserva #%s confirmada.", self.id)  # Registra el evento en el log
        finally:  # Se ejecuta siempre, haya o no error
            logger.debug("Fin del intento de confirmar la reserva #%s.", self.id)  # Deja rastro del intento

    def cancelar(self) -> None:  # Pendiente/Confirmada -> Cancelada
        """Pendiente/Confirmada -> Cancelada."""
        if self._estado in (EstadoReserva.CANCELADA, EstadoReserva.PROCESADA):  # No se cancela si ya terminó
            raise OperacionNoPermitidaError(  # Lanza el error de operación no permitida
                f"No se puede cancelar una reserva {self._estado.value.lower()}."  # Mensaje
            )  # Fin del raise
        self._estado = EstadoReserva.CANCELADA  # Cambia el estado a cancelada
        logger.info("Reserva #%s cancelada.", self.id)  # Registra el evento en el log

    def procesar(self, descuento=None, impuesto=None) -> float:  # Confirmada -> Procesada
        """Confirmada -> Procesada. Calcula y devuelve el costo total."""
        if self._estado != EstadoReserva.CONFIRMADA:  # Solo se procesa una reserva confirmada
            raise OperacionNoPermitidaError(  # Lanza el error de operación no permitida
                f"Solo se procesa una reserva confirmada (estado actual: {self._estado.value})."  # Mensaje
            )  # Fin del raise
        try:  # Intenta calcular el costo
            costo = self._servicio.calcular_costo(self._duracion, descuento, impuesto)  # Cálculo (sobrecarga simulada)
            if costo <= 0:  # Un costo no positivo es inconsistente
                raise CalculoInconsistenteError(f"Costo no válido calculado: {costo}.")  # Lanza el error
        except SoftwareFJError as error:  # Si ocurrió un error propio del sistema
            logger.error("Fallo al procesar la reserva #%s: %s", self.id, error)  # Registra el error
            raise ReservaInvalidaError(f"No se pudo procesar la reserva #{self.id}.") from error  # Excepción encadenada
        else:  # Se ejecuta solo si no hubo error
            self._estado = EstadoReserva.PROCESADA  # Cambia el estado a procesada
            self._costo_total = costo  # Guarda el costo total
            logger.info("Reserva #%s procesada. Costo total: %.2f", self.id, costo)  # Registra el evento
            return costo  # Devuelve el costo calculado
        finally:  # Se ejecuta siempre
            logger.debug("Fin del intento de procesar la reserva #%s.", self.id)  # Deja rastro del intento

    def describir(self) -> str:  # Implementa el método abstracto de EntidadBase
        costo = f" | Total: ${self._costo_total:,.2f}" if self._costo_total is not None else ""  # Texto del costo, si existe
        return (  # Devuelve la descripción de la reserva
            f"Reserva #{self.id} [{self._estado.value}] | {self._cliente.nombre} -> "  # Id, estado y cliente
            f"{self._servicio.nombre} x {self._duracion}{costo}"  # Servicio, duración y costo
        )  # Fin de la descripción
