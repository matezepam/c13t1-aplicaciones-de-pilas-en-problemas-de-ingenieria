# PROBLEMA 4 ORDEN DE RENDERIZADO
# Cada superficie tiene una distancia constante al espectador, representando
# capas frontales sin intersecciones para estudiar el orden de dibujado con una pila.

from math import isfinite


# Valida las distancias y prepara una pila con la superficie más lejana arriba.
# Ordenar primero permite recibir superficies desordenadas y obtener después
# una secuencia de dibujo de lejos a cerca.
def preparar_pila(superficies):
    for superficie in superficies:
        distancia = superficie["distancia"]
        if isinstance(distancia, bool) or not isinstance(distancia, (int, float)):
            raise ValueError("La distancia debe ser numérica")
        if not isfinite(distancia) or distancia <= 0:
            raise ValueError("La distancia debe ser finita y mayor que cero")

    lejanas_primero = sorted(superficies, key=lambda superficie: superficie["distancia"], reverse=True)
    pila = []
    # Apilar de cerca a lejos deja la más lejana en el tope. Al hacer pop, las
    # cercanas salen al final y pueden cubrir las lejanas en este modelo de capas.
    for superficie in reversed(lejanas_primero):
        pila.append(superficie)
    return pila


# Extrae desde el tope y devuelve el orden de dibujo. Conserva referencias
# a las superficies originales para mostrar el resultado sin duplicar sus datos.
def renderizar(pila):
    dibujadas = []
    while pila:
        dibujadas.append(pila.pop())
    return dibujadas


def demostracion():
    superficies = [
        {"nombre": "Panel cercano", "distancia": 2},
        {"nombre": "Pared lejana", "distancia": 10},
        {"nombre": "Estante intermedio", "distancia": 6},
    ]
    print("PROBLEMA 4 ORDEN DE RENDERIZADO")
    print("Entrada:", [(s["nombre"], s["distancia"]) for s in superficies])
    pila = preparar_pila(superficies)
    if pila:
        print("Tope antes de dibujar:", pila[-1]["nombre"])  # Peek sin retirar
    for superficie in renderizar(pila):
        print(f"Dibujar: {superficie['nombre']} | Distancia: {superficie['distancia']}")
    print("Pila vacía:", not pila)


if __name__ == "__main__":
    demostracion()
