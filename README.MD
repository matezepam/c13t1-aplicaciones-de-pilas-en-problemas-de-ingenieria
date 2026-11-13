# C13T1 Aplicaciones de pilas en problemas de ingeniería

Los cinco programas utilizan listas de Python como pilas y trabajan desde su último elemento, con `append` para apilar o **push**, `pop` para retirar o **pop** y `pila[-1]` para consultar el **peek**, comprobando antes si existen elementos para evitar retirar datos de una pila vacía.

## Ejecución

Clona el repositorio y entra a su carpeta:

```bash
git clone https://github.com/matezepam/c13t1-aplicaciones-de-pilas-en-problemas-de-ingenieria.git
cd c13t1-aplicaciones-de-pilas-en-problemas-de-ingenieria
```

Ejecuta el problema que quieras revisar con Python, sin instalar bibliotecas adicionales.

```bash
python "PROBLEMA 1 ROBOT.py"
python "PROBLEMA 2 SINTAXIS.py"
python "PROBLEMA 3 PROTOCOLOS.py"
python "PROBLEMA 4 RENDERIZADO.py"
python "PROBLEMA 5 INTERRUPCIONES.py"
```

Cada archivo funciona por separado y ejecuta los datos de `demostracion`, donde puedes cambiar las entradas para probar otros recorridos, fragmentos de código, mensajes, superficies o prioridades, manteniendo las funciones disponibles para reutilizarlas sin ejecutar la demostración al importarlas.

## Problema 1. Robot de almacén

El robot tiene coordenadas `x`, `y` y una orientación y cada avance recorre una celda, mientras los giros cambian noventa grados y la pila guarda únicamente movimientos completados, dejando fuera el avance bloqueado por el obstáculo para no intentar deshacer una acción que nunca ocurrió.

`realizar_movimiento` recibe el robot, su historial, una acción y la detección simulada de obstáculo y devuelve si pudo ejecutarla, mientras `deshacer_movimiento` consulta el tope y aplica su inverso antes de retirarlo, convirtiendo avanzar en retroceder y cada giro en el giro contrario.

El modelo permite retroceder sin cambiar la orientación y supone que los tramos ya recorridos siguen libres, utilizando la pila para regresar por esos mismos tramos y recuperar también la orientación inicial.

**Entrada:** `Avanzar, Girar Derecha, Avanzar, Avanzar, Girar Izquierda, Avanzar`, seguida de un obstáculo en el siguiente avance.

```text
Antes del obstáculo: (2, 2) | Norte
Obstáculo en el siguiente avance, se deshace la ruta
Retroceder -> (2, 1) | Norte
Girar Derecha -> (2, 1) | Este
Retroceder -> (1, 1) | Este
Retroceder -> (0, 1) | Este
Girar Izquierda -> (0, 1) | Norte
Retroceder -> (0, 0) | Norte
Movimientos pendientes: 0
```

**Complejidad:** con `n` movimientos ejecutados, registrar la ruta y deshacerla requieren **O(n)** tiempo y el historial ocupa **O(n)** espacio, mientras el estado del robot mantiene un tamaño fijo y cada paso de avance, giro o consulta del tope tiene coste constante, con inserción amortizada al usar listas de Python.

## Problema 2. Validador de sintaxis

La pila guarda pares de símbolo de apertura y posición y cada cierre se compara con el tope antes de retirarlo, de modo que `([)]` se rechaza aunque tenga la misma cantidad de aperturas y cierres, porque el orden de anidación es incorrecto.

`validar_sintaxis` recibe un texto y devuelve un booleano y un mensaje con el resultado, ignorando comentarios de estilo Python iniciados con `#` y texto entre comillas simples, dobles o triples, incluyendo escapes, para no confundir sus caracteres con delimitadores del código.

El ejercicio comprueba delimitadores y textos sin cerrar y no ejecuta el código ni comprueba toda la gramática de un lenguaje, manteniendo el enfoque en el uso de la pila.

| Entrada | Resultado esperado |
|---|---|
| `resultado = funcion([1, 2], {'x': 3})` | Válido |
| `([)]` | Cierre `)` incompatible con `[` de posición 2 |
| `datos = [1, 2` | Apertura `[` sin cierre en posición 9 |
| `print("]") # Este } es un comentario` | Válido |
| `)` | Cierre sin apertura en posición 1 |

**Complejidad:** se recorren `n` caracteres en **O(n)** tiempo y se almacenan hasta `d` aperturas pendientes, utilizando **O(d)** espacio auxiliar y **O(n)** en el peor caso, sin guardar una copia completa del código y con `d` igual a su máxima profundidad de anidación.

## Problema 3. Protocolos por capas

La base de la pila contiene el mensaje y sobre ella se agregan las cabeceras de TCP, IP y Ethernet, simulando el paso de una capa interna hacia una externa para que el receptor retire primero la última que se añadió.

`encapsular` recibe un mensaje y las capas y devuelve el paquete como pila de tuplas, mientras `desencapsular` consume esa pila y devuelve el mensaje recuperado y la lista de capas retiradas, comprobando el nombre esperado en el tope y rechazando paquetes incompletos o con un orden incorrecto.

Las cabeceras son etiquetas didácticas y no paquetes binarios enviados por una red, compartiendo el texto del mensaje en lugar de copiar su contenido en cada nivel y conservando una sola capa de datos debajo de las cabeceras.

**Entrada:** `Temperatura del almacén: 24 °C`, con capas TCP, IP y Ethernet.

```text
Pila de base a tope: ['Datos', 'TCP', 'IP', 'Ethernet']
Primera capa que recibirá el receptor: Ethernet
Orden de desencapsulación: Ethernet -> IP -> TCP
Mensaje recuperado: Temperatura del almacén: 24 °C
Pila vacía: True
```

**Complejidad:** para `k` cabeceras de tamaño fijo, encapsular y desencapsular requieren **O(k)** tiempo y las pilas y la lista de capas retiradas utilizan **O(k)** espacio, mientras contar también el mensaje de `m` caracteres da **O(k + m)** almacenamiento total y mostrar el contenido completo requiere tiempo proporcional a esos datos.

## Problema 4. Orden de renderizado

Cada superficie se representa con un nombre y una distancia positiva y `preparar_pila` las ordena de la más lejana a la más cercana para después apilarlas en sentido contrario, dejando la lejana en el tope y permitiendo que `renderizar` las retire en el orden de dibujo correcto.

La pila resuelve el orden de extracción y el ordenamiento establece previamente las distancias, representando capas frontales a distancia constante y sin intersecciones para que las cercanas se dibujen al final y cubran las lejanas cuando coincidan en la vista.

La demostración muestra la secuencia de dibujo en consola y no modela superficies que se cruzan entre sí, donde una única distancia por superficie no bastaría para determinar toda la oclusión.

**Entrada:** panel cercano a distancia `2`, pared lejana a `10` y estante intermedio a `6`.

```text
Tope antes de dibujar: Pared lejana
Dibujar: Pared lejana | Distancia: 10
Dibujar: Estante intermedio | Distancia: 6
Dibujar: Panel cercano | Distancia: 2
Pila vacía: True
```

**Complejidad:** con `n` superficies, la validación, el apilado y la extracción requieren **O(n)** tiempo y el ordenamiento domina con **O(n log n)** en el peor caso, utilizando **O(n)** espacio adicional para las listas de orden, pila y resultado que conservan referencias a las superficies originales.

## Problema 5. Interrupciones anidadas

El procesador se representa con tarea, prioridad, contador de programa `pc` y un registro entero y una solicitud sólo interrumpe si su prioridad es mayor que la actual, guardando una copia del contexto para que los cambios de la nueva tarea no alteren el estado suspendido.

`iniciar_interrupcion` recibe el procesador, la pila, el nombre, la prioridad y la dirección del manejador y devuelve si pudo comenzar, mientras `ejecutar_paso` modifica el contexto activo y `finalizar_interrupcion` retira el último contexto suspendido y lo restaura completo, devolviendo `None` si no existe uno anterior.

Un número mayor significa más prioridad y las solicitudes de prioridad igual o inferior se rechazan en esta simulación sin cambiar la ejecución actual, pudiendo volver a solicitarse después y sin mantener una cola adicional de pendientes.

**Entrada:** temporizador con prioridad `2`, sensor con `5` y emergencia con `9`, seguidos de una solicitud de prioridad `3` mientras está activa la emergencia.

```text
Inicio: Programa principal | prioridad 0 | PC 100 | registro 7
Atendiendo: Temporizador | prioridad 2 | PC 1001 | registro 1
Atendiendo: Sensor | prioridad 5 | PC 2001 | registro 1
Atendiendo: Emergencia | prioridad 9 | PC 3001 | registro 1
Solicitud de prioridad 3 aceptada: False
Siguiente contexto suspendido: Sensor
Restaurado: Sensor | prioridad 5 | PC 2001 | registro 1
Siguiente contexto suspendido: Temporizador
Restaurado: Temporizador | prioridad 2 | PC 1001 | registro 1
Siguiente contexto suspendido: Programa principal
Restaurado: Programa principal | prioridad 0 | PC 100 | registro 7
```

**Complejidad:** cada contexto tiene cuatro campos de tamaño fijo y guardar o restaurar uno requiere **O(1)** tiempo amortizado, con **O(d)** espacio para una profundidad de `d` interrupciones y **O(r)** tiempo para procesar `r` solicitudes y retornos, sin incluir el trabajo propio de los manejadores.

## Operaciones de pila y memoria

En estas implementaciones, `append` y `pop` al final de una lista tienen coste **O(1) amortizado**, porque la lista puede ajustar ocasionalmente su capacidad, mientras consultar el tope, comprobar si está vacía y obtener su longitud requieren **O(1)** tiempo, manteniendo los cálculos y el acceso de la pila separados de la presentación de los ejemplos.
