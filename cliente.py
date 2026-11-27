"""Clase Cliente con validaciones robustas y datos personales encapsulados."""

import re  # Módulo de expresiones regulares (para validar el correo)

from entidad import EntidadBase  # Clase abstracta de la que hereda Cliente
from excepciones import ClienteInvalidoError, ParametroFaltanteError  # Excepciones propias


class Cliente(EntidadBase):  # Cliente hereda de EntidadBase
    """Cliente de Software FJ. Sus datos son privados y se validan al asignarlos."""

    _REGEX_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")  # Patrón básico de un correo válido

    def __init__(self, nombre=None, documento=None, correo=None, telefono=None):  # Constructor con parámetros opcionales
        super().__init__()  # Obtiene el id desde la clase base
        datos = {"nombre": nombre, "documento": documento, "correo": correo, "telefono": telefono}  # Agrupa los datos recibidos
        faltantes = [campo for campo, valor in datos.items() if valor is None]  # Lista los campos que no se enviaron
        if faltantes:  # Si falta algún parámetro obligatorio
            raise ParametroFaltanteError(f"Faltan parámetros del cliente: {', '.join(faltantes)}")  # Lanza el error
        self.nombre = nombre  # Cada asignación pasa por su setter, que valida el dato
        self.documento = documento  # Valida y guarda el documento
        self.correo = correo  # Valida y guarda el correo
        self.telefono = telefono  # Valida y guarda el teléfono

    # ---------- nombre ----------
    @property  # Getter del nombre
    def nombre(self) -> str:  # Permite leer cliente.nombre
        return self.__nombre  # Devuelve el atributo privado (name mangling)

    @nombre.setter  # Setter del nombre
    def nombre(self, valor):  # Se ejecuta al asignar cliente.nombre = ...
        if not isinstance(valor, str) or len(valor.strip()) < 2:  # Debe ser texto de al menos 2 caracteres
            raise ClienteInvalidoError("El nombre debe ser texto de al menos 2 caracteres.")  # Error de validación
        if not all(c.isalpha() or c.isspace() for c in valor):  # Solo letras y espacios
            raise ClienteInvalidoError("El nombre solo puede contener letras y espacios.")  # Error de validación
        self.__nombre = valor.strip().title()  # Guarda el nombre normalizado (Primera Letra Mayúscula)

    # ---------- documento ----------
    @property  # Getter del documento
    def documento(self) -> str:  # Permite leer cliente.documento
        return self.__documento  # Devuelve el atributo privado

    @documento.setter  # Setter del documento
    def documento(self, valor):  # Se ejecuta al asignar cliente.documento = ...
        try:  # Intenta convertir el documento a número
            numero = int(str(valor).strip())  # Conversión a entero
        except (TypeError, ValueError) as error:  # Si no es numérico
            # Encadenamiento de excepciones: se conserva la causa original.
            raise ClienteInvalidoError(f"Documento no numérico: {valor!r}") from error  # raise ... from error
        texto = str(numero)  # Vuelve a texto para medir su longitud
        if not 5 <= len(texto) <= 12 or numero <= 0:  # Debe tener entre 5 y 12 dígitos y ser positivo
            raise ClienteInvalidoError("El documento debe tener entre 5 y 12 dígitos positivos.")  # Error de validación
        self.__documento = texto  # Guarda el documento validado

    # ---------- correo ----------
    @property  # Getter del correo
    def correo(self) -> str:  # Permite leer cliente.correo
        return self.__correo  # Devuelve el atributo privado

    @correo.setter  # Setter del correo
    def correo(self, valor):  # Se ejecuta al asignar cliente.correo = ...
        if not isinstance(valor, str) or not self._REGEX_CORREO.match(valor.strip()):  # Debe cumplir el patrón
            raise ClienteInvalidoError(f"Correo con formato inválido: {valor!r}")  # Error de validación
        self.__correo = valor.strip().lower()  # Guarda el correo en minúsculas

    # ---------- teléfono ----------
    @property  # Getter del teléfono
    def telefono(self) -> str:  # Permite leer cliente.telefono
        return self.__telefono  # Devuelve el atributo privado

    @telefono.setter  # Setter del teléfono
    def telefono(self, valor):  # Se ejecuta al asignar cliente.telefono = ...
        texto = str(valor).strip()  # Convierte a texto y quita espacios
        if not texto.isdigit() or not 7 <= len(texto) <= 10:  # Solo dígitos, de 7 a 10
            raise ClienteInvalidoError(f"Teléfono inválido (7 a 10 dígitos): {valor!r}")  # Error de validación
        self.__telefono = texto  # Guarda el teléfono validado

    def describir(self) -> str:  # Implementa el método abstracto de EntidadBase
        return f"Cliente #{self.id}: {self.nombre} | Doc: {self.documento} | {self.correo} | Tel: {self.telefono}"  # Descripción
