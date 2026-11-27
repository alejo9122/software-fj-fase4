"""Simulación de más de 10 operaciones: válidas e inválidas, sin que el programa se detenga."""

from gestor import GestorSoftwareFJ  # Gestor que administra el sistema
from logger_config import ARCHIVO_LOG, obtener_logger  # Ruta del log y función del logger
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala  # Los tres servicios especializados

logger = obtener_logger()  # Logger compartido


def titulo(numero, texto):  # Imprime el encabezado de cada operación
    print(f"\n--- Operación {numero}: {texto} ---")  # Muestra el número y la descripción


def main():  # Función principal de la simulación
    logger.info("===== Inicio de la simulación Software FJ =====")  # Registra el inicio
    g = GestorSoftwareFJ()  # Crea el gestor (listas vacías)

    titulo(1, "Cliente válido")  # Operación 1
    ana = g.registrar_cliente(nombre="Ana Torres", documento="1094567890", correo="ana@mail.com", telefono="3101234567")  # Cliente válido

    titulo(2, "Cliente con correo inválido")  # Operación 2
    g.registrar_cliente(nombre="Luis Pérez", documento="1234567", correo="luis-sin-arroba", telefono="3001112233")  # Correo sin arroba

    titulo(3, "Cliente con parámetros faltantes")  # Operación 3
    g.registrar_cliente(nombre="Marta Ruiz", documento="9876543")  # Faltan correo y teléfono

    titulo(4, "Cliente con documento no numérico (excepción encadenada)")  # Operación 4
    g.registrar_cliente(nombre="Pedro Gil", documento="ABC123", correo="pedro@mail.com", telefono="3205556677")  # Documento inválido

    titulo(5, "Segundo cliente válido")  # Operación 5
    carlos = g.registrar_cliente(nombre="Carlos Mejía", documento="79123456", correo="carlos@mail.com", telefono="3157778899")  # Válido

    titulo(6, "Servicio válido: sala de reuniones")  # Operación 6
    sala = g.crear_servicio(ReservaSala, "Sala Ejecutiva", 50000, 12)  # Sala válida

    titulo(7, "Servicio inválido: tarifa negativa")  # Operación 7
    g.crear_servicio(ReservaSala, "Sala Fantasma", -100, 5)  # Tarifa negativa

    titulo(8, "Servicio válido: alquiler de equipo")  # Operación 8
    portatiles = g.crear_servicio(AlquilerEquipo, "Portátiles", 30000, "Portátil", 5)  # Alquiler válido

    titulo(9, "Servicio válido: asesoría especializada")  # Operación 9
    asesoria = g.crear_servicio(AsesoriaEspecializada, "Asesoría en Datos", 80000, "Ciencia de datos", "senior")  # Asesoría válida

    titulo(10, "Servicio inválido: nivel de asesoría desconocido")  # Operación 10
    g.crear_servicio(AsesoriaEspecializada, "Asesoría X", 80000, "Redes", "maestro")  # Nivel inexistente

    titulo(11, "Reserva exitosa: crear, confirmar y procesar con descuento e IVA")  # Operación 11
    r1 = g.crear_reserva(ana, sala, 3)  # Reserva de 3 horas
    if r1:  # Si la reserva se creó
        g.ejecutar("Confirmar reserva", r1.confirmar)  # Confirma la reserva
        g.ejecutar("Procesar reserva", r1.procesar, 0.10, 0.19)  # Procesa con 10 % de descuento y 19 % de IVA
        print("  ", r1)  # Muestra la reserva ya procesada

    titulo(12, "Reserva fallida: duración fuera de rango (20 horas)")  # Operación 12
    g.crear_reserva(ana, sala, 20)  # La sala solo permite hasta 8 horas

    titulo(13, "Reserva fallida: cliente inexistente")  # Operación 13
    g.crear_reserva(None, sala, 2)  # Cliente None

    titulo(14, "Reserva fallida: servicio no disponible")  # Operación 14
    proyector = g.crear_servicio(AlquilerEquipo, "Proyectores", 40000, "Proyector", 2, disponible=False)  # Servicio no disponible
    g.crear_reserva(carlos, proyector, 2)  # Intenta reservarlo

    titulo(15, "Operación no permitida: confirmar una reserva ya cancelada")  # Operación 15
    r2 = g.crear_reserva(carlos, portatiles, 8)  # Reserva de 8 días
    if r2:  # Si la reserva se creó
        g.ejecutar("Cancelar reserva", r2.cancelar)  # Cancela la reserva
        g.ejecutar("Confirmar reserva cancelada", r2.confirmar)  # Intenta confirmarla: error controlado

    titulo(16, "Operación no permitida: procesar una reserva sin confirmar")  # Operación 16
    r3 = g.crear_reserva(carlos, asesoria, 2)  # Reserva de 2 horas
    if r3:  # Si la reserva se creó
        g.ejecutar("Procesar reserva pendiente", r3.procesar)  # Intenta procesarla sin confirmar: error controlado

    titulo(17, "Cálculo inconsistente: descuento del 150 %")  # Operación 17
    if r3:  # Si la reserva existe
        g.ejecutar("Confirmar reserva", r3.confirmar)  # La confirma correctamente
        g.ejecutar("Procesar con descuento inválido", r3.procesar, 1.5)  # Descuento de 150 %: error controlado

    titulo(18, "Sobrecarga de costos y polimorfismo")  # Operación 18
    for servicio, duracion in ((sala, 2), (portatiles, 7), (asesoria, 1)):  # Recorre servicios de distinto tipo
        print(f"   {servicio.describir()}")  # Cada servicio se describe a su manera (polimorfismo)
        print(f"     base: {servicio.calcular_costo(duracion):,.2f} | "  # Costo base
              f"descuento 10%: {servicio.calcular_costo(duracion, 0.10):,.2f} | "  # Con descuento
              f"con IVA: {servicio.calcular_costo_con_iva(duracion):,.2f} | "  # Con IVA
              f"desc + IVA: {servicio.calcular_costo(duracion, 0.10, 0.19):,.2f}")  # Con descuento e IVA

    print("\n===== RESUMEN =====")  # Encabezado del resumen
    print(f"Clientes: {len(g.clientes)} | Servicios: {len(g.servicios)} | Reservas: {len(g.reservas)}")  # Totales de las listas
    print(f"Operaciones exitosas: {g.exitos} | Errores controlados: {g.fallos}")  # Totales de éxitos y errores
    print(f"El programa terminó sin interrupciones. Log en: {ARCHIVO_LOG}")  # Mensaje final
    logger.info("===== Fin de la simulación =====")  # Registra el fin


if __name__ == "__main__":  # Solo se ejecuta al correr este archivo directamente
    main()  # Inicia la simulación
