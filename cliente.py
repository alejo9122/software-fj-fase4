"""Clase Cliente con validaciones robustas y datos personales encapsulados."""

import re

from entidad import EntidadBase
from excepciones import ClienteInvalidoError, ParametroFaltanteError


class Cliente(EntidadBase):
    """Cliente de Software FJ. Sus datos son privados y se validan al asignarlos."""

    _REGEX_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")  # Formato básico de correo.

    def __init__(self, nombre=None, documento=None, correo=None, telefono=None):
        super().__init__()  # Obtiene el id desde la clase base.
        datos = {"nombre": nombre, "documento": documento, "correo": correo, "telefono": telefono}
        faltantes = [campo for campo, valor in datos.items() if valor is None]
        if faltantes:  # Si falta algún parámetro obligatorio, se lanza el error.
            raise ParametroFaltanteError(f"Faltan parámetros del cliente: {', '.join(faltantes)}")
        self.nombre = nombre  # Cada asignación pasa por su setter validado.
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    # ---------- nombre ----------
    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 2:
            raise ClienteInvalidoError("El nombre debe ser texto de al menos 2 caracteres.")
        if not all(c.isalpha() or c.isspace() for c in valor):
            raise ClienteInvalidoError("El nombre solo puede contener letras y espacios.")
        self.__nombre = valor.strip().title()  # Se normaliza el formato.

    # ---------- documento ----------
    @property
    def documento(self) -> str:
        return self.__documento

    @documento.setter
    def documento(self, valor):
        try:
            numero = int(str(valor).strip())  # Intenta convertir a número.
        except (TypeError, ValueError) as error:
            # Encadenamiento de excepciones: se conserva la causa original.
            raise ClienteInvalidoError(f"Documento no numérico: {valor!r}") from error
        texto = str(numero)
        if not 5 <= len(texto) <= 12 or numero <= 0:
            raise ClienteInvalidoError("El documento debe tener entre 5 y 12 dígitos positivos.")
        self.__documento = texto

    # ---------- correo ----------
    @property
    def correo(self) -> str:
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or not self._REGEX_CORREO.match(valor.strip()):
            raise ClienteInvalidoError(f"Correo con formato inválido: {valor!r}")
        self.__correo = valor.strip().lower()

    # ---------- teléfono ----------
    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        texto = str(valor).strip()
        if not texto.isdigit() or not 7 <= len(texto) <= 10:
            raise ClienteInvalidoError(f"Teléfono inválido (7 a 10 dígitos): {valor!r}")
        self.__telefono = texto

    def describir(self) -> str:
        return f"Cliente #{self.id}: {self.nombre} | Doc: {self.documento} | {self.correo} | Tel: {self.telefono}"
