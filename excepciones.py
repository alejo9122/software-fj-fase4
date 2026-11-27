"""Excepciones personalizadas del sistema Software FJ.

Todas heredan de SoftwareFJError, de modo que se puedan capturar
de forma general o de forma específica según la necesidad.
"""


class SoftwareFJError(Exception):  # Excepción base: de ella heredan todas las demás
    """Excepción base de todo el sistema."""


class ParametroFaltanteError(SoftwareFJError):  # Se lanza cuando falta un dato obligatorio
    """Se omitió un parámetro obligatorio."""


class ClienteInvalidoError(SoftwareFJError):  # Se lanza cuando un dato del cliente es inválido
    """Los datos de un cliente no cumplen las validaciones."""


class ServicioInvalidoError(SoftwareFJError):  # Se lanza cuando un servicio o su duración son inválidos
    """Los datos o parámetros de un servicio son inválidos."""


class ServicioNoDisponibleError(SoftwareFJError):  # Se lanza cuando el servicio está marcado como no disponible
    """El servicio solicitado no está disponible."""


class ReservaInvalidaError(SoftwareFJError):  # Se lanza cuando una reserva no se puede crear o procesar
    """La reserva no se pudo crear o gestionar correctamente."""


class OperacionNoPermitidaError(SoftwareFJError):  # Se lanza cuando la operación no corresponde al estado actual
    """La operación no es válida para el estado actual del objeto."""


class CalculoInconsistenteError(SoftwareFJError):  # Se lanza cuando un descuento o impuesto es inconsistente
    """Un cálculo de costos produjo valores o parámetros inconsistentes."""
