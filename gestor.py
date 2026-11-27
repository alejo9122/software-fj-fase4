"""Gestor que mantiene las listas internas y ejecuta operaciones sin caerse."""

from cliente import Cliente  # Clase Cliente
from excepciones import SoftwareFJError  # Excepción base del sistema
from logger_config import obtener_logger  # Función que entrega el logger
from reserva import Reserva  # Clase Reserva

logger = obtener_logger()  # Logger compartido para registrar eventos del gestor


class GestorSoftwareFJ:  # Clase que administra todo el sistema en memoria
    """Administra clientes, servicios y reservas en listas (sin base de datos)."""

    def __init__(self):  # Constructor del gestor
        self.clientes = []  # Lista interna de clientes registrados
        self.servicios = []  # Lista interna de servicios creados
        self.reservas = []  # Lista interna de reservas creadas
        self.exitos = 0  # Contador de operaciones exitosas
        self.fallos = 0  # Contador de errores controlados

    def ejecutar(self, descripcion, funcion, *args, **kwargs):  # Ejecuta una operación de forma segura
        """Ejecuta una operación capturando y registrando cualquier error."""
        try:  # Intenta ejecutar la operación
            resultado = funcion(*args, **kwargs)  # Llama a la función con sus argumentos
        except SoftwareFJError as error:  # Captura los errores propios del sistema
            self.fallos += 1  # Suma un error controlado
            causa = f" | causa: {error.__cause__!r}" if error.__cause__ else ""  # Incluye la causa encadenada, si hay
            logger.error("%s -> %s: %s%s", descripcion, type(error).__name__, error, causa)  # Registra el error
            print(f"   [ERROR CONTROLADO] {type(error).__name__}: {error}")  # Muestra el error en pantalla
            return None  # Devuelve None para que el programa continúe
        except Exception as error:  # Red de seguridad para errores inesperados
            self.fallos += 1  # Suma un error controlado
            logger.critical("%s -> error inesperado %s: %s", descripcion, type(error).__name__, error)  # Registra el error
            print(f"   [ERROR INESPERADO CONTROLADO] {type(error).__name__}: {error}")  # Muestra el error
            return None  # Devuelve None para que el programa continúe
        else:  # Se ejecuta solo si no hubo errores
            self.exitos += 1  # Suma una operación exitosa
            logger.info("%s -> OK", descripcion)  # Registra el éxito en el log
            print(f"   [OK] {resultado if resultado is not None else descripcion}")  # Muestra el resultado
            return resultado  # Devuelve el resultado de la operación
        finally:  # Se ejecuta siempre
            logger.debug("Operación finalizada: %s", descripcion)  # Deja rastro de que la operación terminó

    def registrar_cliente(self, **datos):  # Registra un cliente nuevo
        cliente = self.ejecutar("Registrar cliente", Cliente, **datos)  # Intenta crear el cliente de forma segura
        if cliente:  # Si se creó correctamente
            self.clientes.append(cliente)  # Lo agrega a la lista de clientes
        return cliente  # Devuelve el cliente (o None si falló)

    def crear_servicio(self, clase, *args, **kwargs):  # Crea un servicio de cualquier tipo
        servicio = self.ejecutar(f"Crear servicio {clase.__name__}", clase, *args, **kwargs)  # Intenta crearlo
        if servicio:  # Si se creó correctamente
            self.servicios.append(servicio)  # Lo agrega a la lista de servicios
        return servicio  # Devuelve el servicio (o None si falló)

    def crear_reserva(self, cliente, servicio, duracion):  # Crea una reserva nueva
        reserva = self.ejecutar("Crear reserva", Reserva, cliente, servicio, duracion)  # Intenta crearla
        if reserva:  # Si se creó correctamente
            self.reservas.append(reserva)  # La agrega a la lista de reservas
        return reserva  # Devuelve la reserva (o None si falló)
