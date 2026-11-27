"""Clase abstracta Servicio y tres servicios especializados (polimorfismo)."""

from abc import ABC, abstractmethod  # Herramientas para clases y métodos abstractos

from entidad import EntidadBase  # Clase base de las entidades
from excepciones import (  # Excepciones propias que usan los servicios
    CalculoInconsistenteError,  # Descuento o impuesto inconsistente
    ServicioInvalidoError,  # Datos o duración inválidos
    ServicioNoDisponibleError,  # Servicio no disponible
)  # Fin de la importación


class Servicio(EntidadBase, ABC):  # Clase abstracta Servicio
    """Servicio genérico de Software FJ."""

    IVA = 0.19  # Impuesto de referencia para el cálculo con IVA

    def __init__(self, nombre, tarifa_base, disponible=True):  # Constructor común a todos los servicios
        super().__init__()  # Obtiene el id desde EntidadBase
        if not isinstance(nombre, str) or not nombre.strip():  # El nombre no puede estar vacío
            raise ServicioInvalidoError("El nombre del servicio no puede estar vacío.")  # Error de validación
        try:  # Intenta convertir la tarifa a número
            tarifa = float(tarifa_base)  # Acepta números o texto numérico
        except (TypeError, ValueError) as error:  # Si no se puede convertir
            raise ServicioInvalidoError(f"Tarifa no numérica: {tarifa_base!r}") from error  # Excepción encadenada
        if tarifa <= 0:  # La tarifa debe ser positiva
            raise ServicioInvalidoError("La tarifa base debe ser mayor que cero.")  # Error de validación
        self._nombre = nombre.strip()  # Atributo protegido: nombre del servicio
        self._tarifa_base = tarifa  # Atributo protegido: tarifa base
        self._disponible = bool(disponible)  # Atributo protegido: disponibilidad

    @property  # Getter del nombre
    def nombre(self) -> str:  # Permite leer servicio.nombre
        return self._nombre  # Devuelve el nombre

    @property  # Getter de la tarifa
    def tarifa_base(self) -> float:  # Permite leer servicio.tarifa_base
        return self._tarifa_base  # Devuelve la tarifa

    @property  # Getter de la disponibilidad
    def disponible(self) -> bool:  # Permite leer servicio.disponible
        return self._disponible  # Devuelve si está disponible

    @disponible.setter  # Setter de la disponibilidad
    def disponible(self, valor: bool):  # Permite cambiar la disponibilidad
        self._disponible = bool(valor)  # Guarda el nuevo valor como booleano

    # ---------- métodos que cada servicio sobrescribe ----------
    @abstractmethod  # Cada servicio hijo debe implementarlo
    def validar_parametros(self, duracion) -> None:  # Valida la duración y parámetros propios
        """Valida la duración y los parámetros propios del servicio."""

    @abstractmethod  # Cada servicio hijo debe implementarlo
    def calcular_costo_base(self, duracion) -> float:  # Calcula el costo sin descuentos ni impuestos
        """Costo sin descuentos ni impuestos."""

    @abstractmethod  # Cada servicio hijo debe implementarlo
    def describir(self) -> str:  # Describe el servicio
        """Descripción del servicio."""

    # ---------- utilidades compartidas ----------
    def _verificar_disponibilidad(self):  # Comprueba que el servicio esté disponible
        if not self._disponible:  # Si está marcado como no disponible
            raise ServicioNoDisponibleError(f"El servicio '{self._nombre}' no está disponible.")  # Lanza el error

    @staticmethod  # No necesita acceso a self
    def _validar_rango(duracion, minimo, maximo, unidad):  # Valida que la duración sea numérica y esté en rango
        """Comprueba que la duración sea numérica y esté en el rango permitido."""
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):  # Debe ser número (no bool)
            raise ServicioInvalidoError(f"La duración debe ser numérica, se recibió {duracion!r}.")  # Error de tipo
        if not minimo <= duracion <= maximo:  # Debe estar entre el mínimo y el máximo
            raise ServicioInvalidoError(f"Duración fuera de rango: {minimo}-{maximo} {unidad}.")  # Error de rango

    # ---------- método sobrecargado (parámetros opcionales) ----------
    def calcular_costo(self, duracion, descuento=None, impuesto=None) -> float:  # Sobrecarga simulada con parámetros opcionales
        """Sobrecarga simulada con parámetros opcionales:
        calcular_costo(d)                  -> costo base
        calcular_costo(d, 0.10)            -> con descuento
        calcular_costo(d, impuesto=0.19)   -> con impuesto
        calcular_costo(d, 0.10, 0.19)      -> con descuento e impuesto
        """
        self.validar_parametros(duracion)  # Valida antes de calcular (método sobrescrito por cada hijo)
        costo = self.calcular_costo_base(duracion)  # Costo base (polimorfismo: depende del servicio)
        if descuento is not None:  # Si se envió un descuento
            if not isinstance(descuento, (int, float)) or not 0 <= descuento < 1:  # Debe estar en [0, 1)
                raise CalculoInconsistenteError(f"Descuento inconsistente: {descuento!r} (debe estar en [0, 1)).")  # Error
            costo *= 1 - descuento  # Aplica el descuento
        if impuesto is not None:  # Si se envió un impuesto
            if not isinstance(impuesto, (int, float)) or impuesto < 0:  # No puede ser negativo
                raise CalculoInconsistenteError(f"Impuesto inconsistente: {impuesto!r}.")  # Error
            costo *= 1 + impuesto  # Aplica el impuesto
        return round(costo, 2)  # Devuelve el costo redondeado a 2 decimales

    def calcular_costo_con_iva(self, duracion) -> float:  # Variante de cálculo con IVA por defecto
        """Variante de cálculo que aplica el IVA por defecto."""
        return self.calcular_costo(duracion, impuesto=self.IVA)  # Reutiliza calcular_costo con el IVA


class ReservaSala(Servicio):  # Servicio hijo 1: reserva de salas
    """Reserva de salas (se cobra por hora)."""

    def __init__(self, nombre, tarifa_por_hora, capacidad, disponible=True):  # Constructor de la sala
        super().__init__(nombre, tarifa_por_hora, disponible)  # Reutiliza el constructor del padre
        if not isinstance(capacidad, int) or capacidad <= 0:  # La capacidad debe ser entero positivo
            raise ServicioInvalidoError("La capacidad de la sala debe ser un entero positivo.")  # Error de validación
        self._capacidad = capacidad  # Guarda la capacidad de la sala

    def validar_parametros(self, horas) -> None:  # Sobrescribe la validación
        self._verificar_disponibilidad()  # Comprueba que esté disponible
        self._validar_rango(horas, 1, 8, "horas")  # Permite de 1 a 8 horas

    def calcular_costo_base(self, horas) -> float:  # Sobrescribe el cálculo del costo base
        return self._tarifa_base * horas  # Tarifa por hora multiplicada por las horas

    def describir(self) -> str:  # Sobrescribe la descripción
        return f"Sala '{self._nombre}' | Capacidad: {self._capacidad} personas | ${self._tarifa_base:,.0f}/hora"  # Texto


class AlquilerEquipo(Servicio):  # Servicio hijo 2: alquiler de equipos
    """Alquiler de equipos (se cobra por día y por unidad)."""

    def __init__(self, nombre, tarifa_por_dia, equipo, cantidad=1, disponible=True):  # Constructor del alquiler
        super().__init__(nombre, tarifa_por_dia, disponible)  # Reutiliza el constructor del padre
        if not isinstance(equipo, str) or not equipo.strip():  # El equipo debe tener nombre
            raise ServicioInvalidoError("Debe indicar el tipo de equipo.")  # Error de validación
        if not isinstance(cantidad, int) or cantidad <= 0:  # La cantidad debe ser entero positivo
            raise ServicioInvalidoError("La cantidad de equipos debe ser un entero positivo.")  # Error de validación
        self._equipo = equipo.strip()  # Guarda el tipo de equipo
        self._cantidad = cantidad  # Guarda la cantidad de equipos

    def validar_parametros(self, dias) -> None:  # Sobrescribe la validación
        self._verificar_disponibilidad()  # Comprueba que esté disponible
        self._validar_rango(dias, 1, 30, "días")  # Permite de 1 a 30 días

    def calcular_costo_base(self, dias) -> float:  # Sobrescribe el cálculo del costo base
        costo = self._tarifa_base * dias * self._cantidad  # Tarifa por día, por días y por unidades
        if dias >= 7:  # Si el alquiler es de una semana o más
            costo *= 0.90  # Descuento del 10 % por alquiler semanal
        return costo  # Devuelve el costo base

    def describir(self) -> str:  # Sobrescribe la descripción
        return f"Alquiler de {self._cantidad} x {self._equipo} | ${self._tarifa_base:,.0f}/día"  # Texto descriptivo


class AsesoriaEspecializada(Servicio):  # Servicio hijo 3: asesorías especializadas
    """Asesorías especializadas (por hora, con recargo según el nivel)."""

    RECARGOS = {"junior": 1.0, "senior": 1.5, "experto": 2.0}  # Multiplicador de tarifa según el nivel

    def __init__(self, nombre, tarifa_por_hora, especialidad, nivel="junior", disponible=True):  # Constructor
        super().__init__(nombre, tarifa_por_hora, disponible)  # Reutiliza el constructor del padre
        if not isinstance(especialidad, str) or not especialidad.strip():  # La especialidad no puede estar vacía
            raise ServicioInvalidoError("Debe indicar la especialidad de la asesoría.")  # Error de validación
        if nivel not in self.RECARGOS:  # El nivel debe ser uno de los permitidos
            raise ServicioInvalidoError(f"Nivel inválido: {nivel!r}. Opciones: {', '.join(self.RECARGOS)}.")  # Error
        self._especialidad = especialidad.strip()  # Guarda la especialidad
        self._nivel = nivel  # Guarda el nivel del asesor

    def validar_parametros(self, horas) -> None:  # Sobrescribe la validación
        self._verificar_disponibilidad()  # Comprueba que esté disponible
        self._validar_rango(horas, 0.5, 4, "horas")  # Permite de 0,5 a 4 horas

    def calcular_costo_base(self, horas) -> float:  # Sobrescribe el cálculo del costo base
        return self._tarifa_base * horas * self.RECARGOS[self._nivel]  # Tarifa por horas y por recargo del nivel

    def describir(self) -> str:  # Sobrescribe la descripción
        return f"Asesoría de {self._especialidad} (nivel {self._nivel}) | ${self._tarifa_base:,.0f}/hora base"  # Texto
