"""Configuración del archivo de logs (único uso de archivos del sistema)."""

import logging
import os

# Carpeta y archivo donde se guardan los eventos y errores.
DIRECTORIO_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
ARCHIVO_LOG = os.path.join(DIRECTORIO_LOGS, "sistema.log")


def obtener_logger() -> logging.Logger:
    """Devuelve el logger del sistema, configurándolo solo la primera vez."""
    logger = logging.getLogger("software_fj")  # Logger con nombre propio.
    if logger.handlers:  # Si ya fue configurado, se reutiliza.
        return logger
    os.makedirs(DIRECTORIO_LOGS, exist_ok=True)  # Crea la carpeta si no existe.
    logger.setLevel(logging.DEBUG)  # Registra todos los niveles.
    formato = logging.Formatter("%(asctime)s | %(levelname)-8s | %(module)s | %(message)s")
    manejador = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")  # Escribe en archivo.
    manejador.setFormatter(formato)  # Aplica el formato.
    logger.addHandler(manejador)  # Asocia el manejador al logger.
    return logger
