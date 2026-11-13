# PROBLEMA 1 NAVEGACIÓN DE UN ROBOT DE ALMACÉN
# La pila conserva sólo los movimientos ejecutados para poder deshacerlos
# desde el último hasta recuperar la posición y orientación de partida.

DIRECCIONES = ("Norte", "Este", "Sur", "Oeste")
DESPLAZAMIENTOS = ((0, 1), (1, 0), (0, -1), (-1, 0))
MOVIMIENTOS = ("Avanzar", "Girar Derecha", "Girar Izquierda")


# Inicializa las coordenadas y la orientación del robot. El historial se crea
# aparte para que cada recorrido conserve sus propios movimientos.
def crear_robot():
    return {"x": 0, "y": 0, "direccion": 0}


# Actualiza posición u orientación según la acción. Retroceder mantiene la
# orientación y recorre hacia atrás el mismo tramo, permitiendo invertir un avance.
def aplicar_movimiento(robot, movimiento):
    if movimiento in ("Avanzar", "Retroceder"):
        paso_x, paso_y = DESPLAZAMIENTOS[robot["direccion"]]
        sentido = 1 if movimiento == "Avanzar" else -1
        robot["x"] += sentido * paso_x
        robot["y"] += sentido * paso_y
    elif movimiento == "Girar Derecha":
        robot["direccion"] = (robot["direccion"] + 1) % 4
    elif movimiento == "Girar Izquierda":
        robot["direccion"] = (robot["direccion"] - 1) % 4
    else:
        raise ValueError("Movimiento desconocido")


# Ejecuta la acción y devuelve si pudo completarse. Sólo apila movimientos
# realizados: guardar un avance bloqueado haría retroceder al robot de más.
def realizar_movimiento(robot, historial, movimiento, obstaculo=False):
    if movimiento not in MOVIMIENTOS:
        raise ValueError("Use Avanzar, Girar Derecha o Girar Izquierda")
    if movimiento == "Avanzar" and obstaculo:
        return False
    aplicar_movimiento(robot, movimiento)
    historial.append(movimiento)  # Push: el movimiento reciente queda en el tope
    return True


# Consulta el último movimiento y aplica su inverso antes de retirarlo.
# El orden LIFO permite volver por los mismos tramos y deshacer también los
# giros, sin tomar un atajo que podría atravesar un obstáculo.
def deshacer_movimiento(robot, historial):
    if not historial:
        return None
    ultimo = historial[-1]  # Peek: mirar el tope todavía no lo elimina
    inversos = {
        "Avanzar": "Retroceder",
        "Girar Derecha": "Girar Izquierda",
        "Girar Izquierda": "Girar Derecha",
    }
    inverso = inversos[ultimo]
    aplicar_movimiento(robot, inverso)
    historial.pop()  # Pop: se retira sólo después de completar la acción inversa
    return inverso


# Resume el estado para que la demostración permita comprobar también los giros.
def mostrar_estado(robot):
    return f"({robot['x']}, {robot['y']}) | {DIRECCIONES[robot['direccion']]}"


def demostracion():
    robot = crear_robot()
    historial = []
    ruta = ["Avanzar", "Girar Derecha", "Avanzar",
            "Avanzar", "Girar Izquierda", "Avanzar"]
    print("PROBLEMA 1 ROBOT DE ALMACÉN")
    print("Entrada:", ruta)
    for movimiento in ruta:
        realizar_movimiento(robot, historial, movimiento)
    print("Antes del obstáculo:", mostrar_estado(robot))
    if not realizar_movimiento(robot, historial, "Avanzar", obstaculo=True):
        print("Obstáculo en el siguiente avance, se deshace la ruta")
        while historial:
            inverso = deshacer_movimiento(robot, historial)
            print(inverso, "->", mostrar_estado(robot))
    print("Movimientos pendientes:", len(historial))


if __name__ == "__main__":
    demostracion()
