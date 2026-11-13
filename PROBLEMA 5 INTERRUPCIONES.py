# PROBLEMA 5 INTERRUPCIONES ANIDADAS
# La pila guarda el estado que se suspende para recuperar primero la tarea
# interrumpida más recientemente y continuar desde su contador de programa.


# Crea un procesador simulado con tarea, prioridad, contador y registro.
# Estos campos permiten comprobar que retomar una tarea recupera también
# su punto de ejecución y sus datos, no solamente su nombre.
def crear_procesador():
    return {"tarea": "Programa principal", "prioridad": 0, "pc": 100, "registro": 7}


# Acepta una interrupción sólo si tiene mayor prioridad que la tarea actual.
# Esto permite anidar las urgentes sin suspenderlas por solicitudes de igual
# o menor importancia; devuelve False cuando no se inicia la nueva tarea.
def iniciar_interrupcion(procesador, pila, nombre, prioridad, direccion):
    if type(prioridad) is not int or prioridad <= 0:
        raise ValueError("La prioridad debe ser un entero positivo")
    if type(direccion) is not int or direccion < 0:
        raise ValueError("La dirección debe ser un entero no negativo")
    if prioridad <= procesador["prioridad"]:
        return False
    # Se apila una copia del contexto suspendido. Si se guardara el mismo
    # diccionario, la nueva interrupción modificaría también los estados anteriores.
    pila.append(procesador.copy())  # Push: guardar la tarea suspendida
    procesador.update(tarea=nombre, prioridad=prioridad, pc=direccion, registro=0)
    return True


# Simula una instrucción que modifica el contador y el registro del contexto
# actual para comprobar después que esos cambios no alteran el estado suspendido.
def ejecutar_paso(procesador):
    procesador["pc"] += 1
    procesador["registro"] += 1


# Recupera el último contexto suspendido y restaura todos sus campos.
# LIFO retoma primero la tarea interrumpida más recientemente; si no hay
# contexto guardado, devuelve None sin cambiar el programa principal.
def finalizar_interrupcion(procesador, pila):
    if not pila:
        return None
    estado_anterior = pila.pop()
    procesador.clear()
    procesador.update(estado_anterior)
    return procesador["tarea"]


def mostrar_estado(procesador):
    return f"{procesador['tarea']} | prioridad {procesador['prioridad']} | PC {procesador['pc']} | registro {procesador['registro']}"


def demostracion():
    procesador = crear_procesador()
    pila = []
    print("PROBLEMA 5 INTERRUPCIONES ANIDADAS")
    print("Inicio:", mostrar_estado(procesador))
    for nombre, prioridad, direccion in (
        ("Temporizador", 2, 1000),
        ("Sensor", 5, 2000),
        ("Emergencia", 9, 3000),
    ):
        iniciar_interrupcion(procesador, pila, nombre, prioridad, direccion)
        ejecutar_paso(procesador)
        print("Atendiendo:", mostrar_estado(procesador))
    aceptada = iniciar_interrupcion(procesador, pila, "Solicitud menor", 3, 4000)
    print("Solicitud de prioridad 3 aceptada:", aceptada)
    while pila:
        print("Siguiente contexto suspendido:", pila[-1]["tarea"])  # Peek
        finalizar_interrupcion(procesador, pila)
        print("Restaurado:", mostrar_estado(procesador))


if __name__ == "__main__":
    demostracion()
