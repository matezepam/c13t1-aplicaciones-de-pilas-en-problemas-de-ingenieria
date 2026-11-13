# PROBLEMA 2 VALIDADOR DE DELIMITADORES
# La pila relaciona cada cierre con la apertura más reciente para comprobar
# tanto el balance como la anidación de paréntesis, corchetes y llaves.

PAREJAS = {")": "(", "]": "[", "}": "{"}


# Devuelve si los delimitadores están balanceados y un mensaje del resultado.
# Apila cada apertura con su posición para comprobar la anidación e indicar
# dónde comenzó el delimitador que causa un error.
def validar_sintaxis(codigo):
    pila = []
    comillas = ""
    indice = 0
    while indice < len(codigo):
        caracter = codigo[indice]

        # Un corchete dentro de un texto no abre una estructura del código.
        # Se omiten los literales y sus escapes para evitar errores de balance falsos.
        if comillas:
            if caracter == "\\":
                indice += 2
            elif codigo.startswith(comillas, indice):
                indice += len(comillas)
                comillas = ""
            else:
                indice += 1
            continue
        if caracter in ("'", '"'):
            comillas = caracter * 3 if codigo.startswith(caracter * 3, indice) else caracter
            indice += len(comillas)
            continue

        # Se consideran comentarios de estilo Python hasta el salto de línea,
        # evitando que un corchete escrito en un comentario cambie el resultado.
        if caracter == "#":
            while indice < len(codigo) and codigo[indice] != "\n":
                indice += 1
            continue

        if caracter in "([{":
            pila.append((caracter, indice + 1))  # Push: recordar apertura y posición
        elif caracter in PAREJAS:
            if not pila:
                return False, f"Cierre {caracter} sin apertura en posición {indice + 1}"
            # El cierre debe coincidir con la apertura más reciente. Contar
            # símbolos no basta: ([)] tiene cantidades iguales y está mal anidado.
            apertura, posicion = pila[-1]  # Peek: comprobar antes de retirar
            if apertura != PAREJAS[caracter]:
                return False, f"Cierre {caracter} incompatible con {apertura} de posición {posicion}"
            pila.pop()  # Pop: se retira únicamente la apertura correspondiente
        indice += 1

    if comillas:
        return False, "Texto entre comillas sin cerrar"
    if pila:
        apertura, posicion = pila[-1]
        return False, f"Apertura {apertura} sin cierre en posición {posicion}"
    return True, "Delimitadores balanceados y correctamente anidados"


def demostracion():
    ejemplos = [
        "resultado = funcion([1, 2], {'x': 3})",
        "([)]",
        "datos = [1, 2",
        'print("]") # Este } es un comentario',
        ")",
    ]
    print("PROBLEMA 2 VALIDADOR DE SINTAXIS")
    for codigo in ejemplos:
        valido, mensaje = validar_sintaxis(codigo)
        print("\nEntrada:", codigo)
        print("Resultado:", "Válido" if valido else "Inválido")
        print(mensaje)


if __name__ == "__main__":
    demostracion()
