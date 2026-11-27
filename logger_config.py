"""Configuración del archivo de logs (único uso de archivos del sistema)."""

import logging  # Módulo estándar de Python para registrar eventos
import os  # Módulo para trabajar con rutas y carpetas

# Carpeta y archivo donde se guardan los eventos y errores.
DIRECTORIO_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")  # Carpeta logs junto a este archivo
ARCHIVO_LOG = os.path.join(DIRECTORIO_LOGS, "sistema.log")  # Ruta completa del archivo de logs


def obtener_logger() -> logging.Logger:  # Función que entrega el logger del sistema
    """Devuelve el logger del sistema, configurándolo solo la primera vez."""
    logger = logging.getLogger("software_fj")  # Obtiene (o crea) el logger con nombre propio
    if logger.handlers:  # Si ya tiene manejadores, ya fue configurado
        return logger  # Se reutiliza sin configurarlo de nuevo
    os.makedirs(DIRECTORIO_LOGS, exist_ok=True)  # Crea la carpeta de logs si no existe
    logger.setLevel(logging.DEBUG)  # Registra todos los niveles (DEBUG, INFO, ERROR, CRITICAL)
    formato = logging.Formatter("%(asctime)s | %(levelname)-8s | %(module)s | %(message)s")  # Fecha | nivel | módulo | mensaje
    manejador = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")  # Manejador que escribe en el archivo
    manejador.setFormatter(formato)  # Aplica el formato al manejador
    logger.addHandler(manejador)  # Asocia el manejador al logger
    return logger  # Devuelve el logger ya configurado
