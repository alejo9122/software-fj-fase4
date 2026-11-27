# Software FJ – Sistema integral de gestión de clientes, servicios y reservas

Proyecto de la Fase 4 del curso Programación (213023) – UNAD.
Sistema orientado a objetos en Python, sin base de datos, con manejo avanzado de excepciones y archivo de logs.

## Cómo ejecutar
```bash
python main.py
```
Requiere Python 3.8 o superior. No usa librerías externas. Los eventos y errores quedan en `logs/sistema.log`.

## Estructura
| Archivo | Contenido |
|---|---|
| `entidad.py` | Clase abstracta `EntidadBase` |
| `cliente.py` | `Cliente` con atributos privados y validaciones |
| `servicios.py` | `Servicio` (abstracta) + `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada` |
| `reserva.py` | `Reserva` y `EstadoReserva` (confirmar, cancelar, procesar) |
| `excepciones.py` | Excepciones personalizadas (`SoftwareFJError` y derivadas) |
| `logger_config.py` | Configuración del archivo de logs |
| `gestor.py` | Listas internas y ejecución segura de operaciones |
| `main.py` | Simulación de más de 10 operaciones válidas e inválidas |

## Conceptos aplicados
- **Abstracción:** `EntidadBase` y `Servicio` son clases abstractas (`ABC`).
- **Herencia y polimorfismo:** los tres servicios sobrescriben `validar_parametros`, `calcular_costo_base` y `describir`.
- **Encapsulación:** atributos privados con propiedades y setters validados en `Cliente`.
- **Sobrecarga simulada:** `calcular_costo(duracion, descuento=None, impuesto=None)` y `calcular_costo_con_iva`.
- **Excepciones:** personalizadas, `try/except`, `try/except/else`, `try/except/finally` y encadenamiento con `raise ... from`.
- **Logs:** `logging` escribe todos los eventos y errores en `logs/sistema.log`.

## Autor
Alejandro Felipe Mazo Ocampo. Por motivos personales solicitó un plazo para presentar esta actividad colaborativa, por lo que la desarrolló de forma individual, asumiendo todos los roles del grupo.
