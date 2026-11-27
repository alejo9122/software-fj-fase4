"""Gestor que mantiene las listas internas y ejecuta operaciones sin caerse."""

from cliente import Cliente
from excepciones import SoftwareFJError
from logger_config import obtener_logger
from reserva import Reserva

logger = obtener_logger()


class GestorSoftwareFJ:
    """Administra clientes, servicios y reservas en listas (sin base de datos)."""

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []
        self.exitos = 0
        self.fallos = 0

    def ejecutar(self, descripcion, funcion, *args, **kwargs):
        """Ejecuta una operación capturando y registrando cualquier error."""
        try:
            resultado = funcion(*args, **kwargs)
        except SoftwareFJError as error:
            self.fallos += 1
            causa = f" | causa: {error.__cause__!r}" if error.__cause__ else ""
            logger.error("%s -> %s: %s%s", descripcion, type(error).__name__, error, causa)
            print(f"   [ERROR CONTROLADO] {type(error).__name__}: {error}")
            return None
        except Exception as error:  # Red de seguridad para errores inesperados.
            self.fallos += 1
            logger.critical("%s -> error inesperado %s: %s", descripcion, type(error).__name__, error)
            print(f"   [ERROR INESPERADO CONTROLADO] {type(error).__name__}: {error}")
            return None
        else:
            self.exitos += 1
            logger.info("%s -> OK", descripcion)
            print(f"   [OK] {resultado if resultado is not None else descripcion}")
            return resultado
        finally:
            logger.debug("Operación finalizada: %s", descripcion)

    def registrar_cliente(self, **datos):
        cliente = self.ejecutar("Registrar cliente", Cliente, **datos)
        if cliente:
            self.clientes.append(cliente)
        return cliente

    def crear_servicio(self, clase, *args, **kwargs):
        servicio = self.ejecutar(f"Crear servicio {clase.__name__}", clase, *args, **kwargs)
        if servicio:
            self.servicios.append(servicio)
        return servicio

    def crear_reserva(self, cliente, servicio, duracion):
        reserva = self.ejecutar("Crear reserva", Reserva, cliente, servicio, duracion)
        if reserva:
            self.reservas.append(reserva)
        return reserva
