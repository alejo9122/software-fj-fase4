"""Excepciones personalizadas del sistema Software FJ.

Todas heredan de SoftwareFJError, de modo que se puedan capturar
de forma general o de forma específica según la necesidad.
"""


class SoftwareFJError(Exception):
    """Excepción base de todo el sistema."""


class ParametroFaltanteError(SoftwareFJError):
    """Se omitió un parámetro obligatorio."""


class ClienteInvalidoError(SoftwareFJError):
    """Los datos de un cliente no cumplen las validaciones."""


class ServicioInvalidoError(SoftwareFJError):
    """Los datos o parámetros de un servicio son inválidos."""


class ServicioNoDisponibleError(SoftwareFJError):
    """El servicio solicitado no está disponible."""


class ReservaInvalidaError(SoftwareFJError):
    """La reserva no se pudo crear o gestionar correctamente."""


class OperacionNoPermitidaError(SoftwareFJError):
    """La operación no es válida para el estado actual del objeto."""


class CalculoInconsistenteError(SoftwareFJError):
    """Un cálculo de costos produjo valores o parámetros inconsistentes."""
