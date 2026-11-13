# PROBLEMA 3 ENCAPSULACIÓN POR CAPAS
# Las cabeceras se representan mediante tuplas sobre los datos, dejando la
# última capa agregada en el tope para que sea la primera que retire el receptor.

CAPAS = (
    ("TCP", "Puerto destino: 5000"),
    ("IP", "Destino: 192.0.2.10"),
    ("Ethernet", "Destino: equipo receptor"),
)


# Construye la pila desde los datos hacia la capa exterior. Así, la última
# cabecera añadida queda lista para retirarse primero al recibir el paquete.
# El mensaje se conserva una sola vez para evitar copias por cada capa.
def encapsular(mensaje, capas=CAPAS):
    paquete = [("Datos", mensaje)]
    for nombre, cabecera in capas:
        paquete.append((nombre, cabecera))  # Push: una capa más externa
    return paquete


# Retira las capas exteriores primero y devuelve el mensaje con el orden de
# desencapsulación. Comprobar el tope permite rechazar capas faltantes o mal
# ordenadas antes de retirar la cabecera que no corresponde.
def desencapsular(paquete, capas=CAPAS):
    retiradas = []
    for nombre, cabecera in reversed(capas):
        if not paquete or paquete[-1][0] != nombre:  # Peek con comprobación de vacío
            raise ValueError(f"Paquete inválido, se esperaba la capa {nombre}")
        retiradas.append(paquete.pop()[0])  # Pop: retirar desde la capa exterior
    if len(paquete) != 1 or paquete[-1][0] != "Datos":
        raise ValueError("El paquete no contiene únicamente los datos originales")
    mensaje = paquete.pop()[1]
    return mensaje, retiradas


def demostracion():
    mensaje = "Temperatura del almacén: 24 °C"
    paquete = encapsular(mensaje)
    print("PROBLEMA 3 PROTOCOLOS POR CAPAS")
    print("Entrada:", mensaje)
    print("Pila de base a tope:", [capa for capa, contenido in paquete])
    print("Primera capa que recibirá el receptor:", paquete[-1][0])
    recuperado, retiradas = desencapsular(paquete)
    print("Orden de desencapsulación:", " -> ".join(retiradas))
    print("Mensaje recuperado:", recuperado)
    print("Pila vacía:", not paquete)


if __name__ == "__main__":
    demostracion()
