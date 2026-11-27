"""Simulación de más de 10 operaciones: válidas e inválidas, sin que el programa se detenga."""

from gestor import GestorSoftwareFJ
from logger_config import ARCHIVO_LOG, obtener_logger
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala

logger = obtener_logger()


def titulo(numero, texto):
    print(f"\n--- Operación {numero}: {texto} ---")


def main():
    logger.info("===== Inicio de la simulación Software FJ =====")
    g = GestorSoftwareFJ()

    titulo(1, "Cliente válido")
    ana = g.registrar_cliente(nombre="Ana Torres", documento="1094567890", correo="ana@mail.com", telefono="3101234567")

    titulo(2, "Cliente con correo inválido")
    g.registrar_cliente(nombre="Luis Pérez", documento="1234567", correo="luis-sin-arroba", telefono="3001112233")

    titulo(3, "Cliente con parámetros faltantes")
    g.registrar_cliente(nombre="Marta Ruiz", documento="9876543")

    titulo(4, "Cliente con documento no numérico (excepción encadenada)")
    g.registrar_cliente(nombre="Pedro Gil", documento="ABC123", correo="pedro@mail.com", telefono="3205556677")

    titulo(5, "Segundo cliente válido")
    carlos = g.registrar_cliente(nombre="Carlos Mejía", documento="79123456", correo="carlos@mail.com", telefono="3157778899")

    titulo(6, "Servicio válido: sala de reuniones")
    sala = g.crear_servicio(ReservaSala, "Sala Ejecutiva", 50000, 12)

    titulo(7, "Servicio inválido: tarifa negativa")
    g.crear_servicio(ReservaSala, "Sala Fantasma", -100, 5)

    titulo(8, "Servicio válido: alquiler de equipo")
    portatiles = g.crear_servicio(AlquilerEquipo, "Portátiles", 30000, "Portátil", 5)

    titulo(9, "Servicio válido: asesoría especializada")
    asesoria = g.crear_servicio(AsesoriaEspecializada, "Asesoría en Datos", 80000, "Ciencia de datos", "senior")

    titulo(10, "Servicio inválido: nivel de asesoría desconocido")
    g.crear_servicio(AsesoriaEspecializada, "Asesoría X", 80000, "Redes", "maestro")

    titulo(11, "Reserva exitosa: crear, confirmar y procesar con descuento e IVA")
    r1 = g.crear_reserva(ana, sala, 3)
    if r1:
        g.ejecutar("Confirmar reserva", r1.confirmar)
        g.ejecutar("Procesar reserva", r1.procesar, 0.10, 0.19)
        print("  ", r1)

    titulo(12, "Reserva fallida: duración fuera de rango (20 horas)")
    g.crear_reserva(ana, sala, 20)

    titulo(13, "Reserva fallida: cliente inexistente")
    g.crear_reserva(None, sala, 2)

    titulo(14, "Reserva fallida: servicio no disponible")
    proyector = g.crear_servicio(AlquilerEquipo, "Proyectores", 40000, "Proyector", 2, disponible=False)
    g.crear_reserva(carlos, proyector, 2)

    titulo(15, "Operación no permitida: confirmar una reserva ya cancelada")
    r2 = g.crear_reserva(carlos, portatiles, 8)
    if r2:
        g.ejecutar("Cancelar reserva", r2.cancelar)
        g.ejecutar("Confirmar reserva cancelada", r2.confirmar)

    titulo(16, "Operación no permitida: procesar una reserva sin confirmar")
    r3 = g.crear_reserva(carlos, asesoria, 2)
    if r3:
        g.ejecutar("Procesar reserva pendiente", r3.procesar)

    titulo(17, "Cálculo inconsistente: descuento del 150 %")
    if r3:
        g.ejecutar("Confirmar reserva", r3.confirmar)
        g.ejecutar("Procesar con descuento inválido", r3.procesar, 1.5)

    titulo(18, "Sobrecarga de costos y polimorfismo")
    for servicio, duracion in ((sala, 2), (portatiles, 7), (asesoria, 1)):
        print(f"   {servicio.describir()}")
        print(f"     base: {servicio.calcular_costo(duracion):,.2f} | "
              f"descuento 10%: {servicio.calcular_costo(duracion, 0.10):,.2f} | "
              f"con IVA: {servicio.calcular_costo_con_iva(duracion):,.2f} | "
              f"desc + IVA: {servicio.calcular_costo(duracion, 0.10, 0.19):,.2f}")

    print("\n===== RESUMEN =====")
    print(f"Clientes: {len(g.clientes)} | Servicios: {len(g.servicios)} | Reservas: {len(g.reservas)}")
    print(f"Operaciones exitosas: {g.exitos} | Errores controlados: {g.fallos}")
    print(f"El programa terminó sin interrupciones. Log en: {ARCHIVO_LOG}")
    logger.info("===== Fin de la simulación =====")


if __name__ == "__main__":
    main()
