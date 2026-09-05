# Agente Mapu: busqueda BFS y DFS

Aplicacion en Python y PyGame para resolver el problema de los aldeanos y verdugos mediante busqueda no informada. El juego permite seleccionar BFS o DFS desde la interfaz, visualizar la asistencia paso a paso y consultar las metricas en la terminal.

## Problema

El objetivo es transportar tres aldeanos y tres verdugos desde la orilla izquierda hasta la derecha. La barca transporta uno o dos personajes por viaje.

Cada estado se representa como:

```text
[aldeanos_izquierda, verdugos_izquierda, barca_izquierda]
```

- `barca_izquierda = 1`: la barca esta en la izquierda.
- `barca_izquierda = 0`: la barca esta en la derecha.
- Estado inicial: `[3, 3, 1]`.
- Estado objetivo: `[0, 0, 0]`.

Un estado es valido cuando, en cada orilla que tenga aldeanos, los verdugos no superan a los aldeanos.

## Implementacion

La funcion `pasa_aa()` genera los sucesores validos usando las cinco tripulaciones posibles:

- un aldeano;
- dos aldeanos;
- un verdugo;
- dos verdugos;
- un aldeano y un verdugo.

La funcion `es_estado_valido()` valida las restricciones de ambas orillas. Los estados visitados se almacenan como tuplas para evitar ciclos.

La logica principal se encuentra en [AgenteMapu.py](AgenteMapu.py):

- `_buscar_bfs()`: usa una frontera FIFO y devuelve la primera solucion mas corta.
- `_buscar_dfs()`: usa una pila LIFO y explora una rama antes de retroceder.
- `buscar_solucion()`: permite solicitar explicitamente BFS o DFS.
- `obtener_pasos_asistencia()`: calcula la ruta del algoritmo seleccionado y actualiza el camino y sus metricas.
- `generar_reporte_metricas()`: ejecuta BFS y DFS desde el mismo estado inicial para compararlos.

## BFS y DFS

### BFS

BFS explora el espacio por niveles mediante una frontera FIFO. Como cada movimiento tiene el mismo costo, garantiza una solucion de longitud minima si existe.

### DFS

DFS explora en profundidad mediante una pila LIFO. Puede encontrar una solucion valida sin garantizar que sea la mas corta. La longitud final depende del orden en que se generen los sucesores.

En la configuracion actual, el orden de sucesores hace que BFS y DFS encuentren una ruta de 11 movimientos. Esto es valido: DFS puede coincidir accidentalmente con la solucion optima, aunque no ofrece esa garantia en general.

## Metricas

Para cada busqueda se registran:

- `profundidad`: longitud de la solucion encontrada;
- `nodos_expandidos`: estados extraidos y procesados;
- `espacio_maximo`: mayor cantidad de caminos presentes en la frontera;
- `tiempo`: duracion de la busqueda medida con `time.perf_counter()`.

Las metricas del algoritmo activo se acumulan durante la asistencia y se muestran al terminar la partida. La comparacion BFS/DFS se calcula al final desde el estado inicial y se imprime solamente en la terminal; no se dicta mediante voz.

## Interfaz y flujo de ejecucion

La integracion grafica se encuentra en [Rio.py](Rio.py). La interfaz incluye:

- `AGENTE BFS`: activa BFS para la asistencia de la partida;
- `AGENTE DFS`: activa DFS para la asistencia de la partida;
- `NUEVO`: reinicia la partida;
- control de sonido.

Solo un algoritmo puede estar activo durante una partida. Al pulsar un boton, se calcula la ruta correspondiente y se muestran sus instrucciones por consola y mediante Pyttsx4. La comparacion con el otro algoritmo se presenta despues de alcanzar el estado objetivo.

El entorno no ejecuta una busqueda automaticamente al iniciar. La busqueda comienza cuando el usuario pulsa `AGENTE BFS` o `AGENTE DFS`.

## Ejemplo de resultados

Una ejecucion puede producir una salida similar a:

```text
Solucion completada en 11 movimientos.
Rendimiento BFS: 15 nodos explorados, frontera maxima de 3 estados y 0.000108 segundos.
Longitud de la solucion BFS: 11 movimientos.
Comparacion BFS vs DFS:
BFS: longitud=11, nodos explorados=15, tiempo=0.000282s, frontera maxima=3.
DFS: longitud=11, nodos explorados=13, tiempo=0.000217s, frontera maxima=3.
```

Los tiempos dependen del equipo y de la carga del sistema. En las pruebas realizadas, BFS y DFS encontraron 11 movimientos, mientras que DFS exploro menos nodos con el orden actual de sucesores. Esto no modifica la propiedad teorica de BFS como algoritmo optimo ni convierte a DFS en un algoritmo optimo.

## Complejidad teorica

Sea `b` el factor de ramificacion, `d` la profundidad de la solucion y `m` la profundidad maxima del espacio de estados:

| Algoritmo | Tiempo | Espacio | Optimalidad |
| --- | --- | --- | --- |
| BFS | `O(b^d)` | `O(b^d)` | Si, con costos uniformes |
| DFS | `O(b^m)` | `O(bm)` | No garantizada |

Para este problema hay como maximo `(3 + 1) * (3 + 1) * 2 = 32` combinaciones de estado representadas, aunque solo una parte cumple las restricciones de validez.

## Ejecucion

Instalar dependencias:

```powershell
python -m pip install -r requirements.txt
```

Ejecutar desde la carpeta raiz del proyecto:

```powershell
python main.py
```

El juego necesita las carpetas `imagenes/` y `sonido/`, por lo que deben conservarse las rutas relativas del proyecto.

## Validacion

Ejecutar las pruebas unitarias con:

```powershell
python -m unittest -v test_agente_mapu.py
```

Las pruebas verifican la generacion de sucesores, la validez de los estados, la recalculacion de rutas, la existencia de soluciones BFS y DFS y la generacion del reporte comparativo.

## Estructura principal

```text
AgenteMapu.py       Logica del agente, BFS, DFS y metricas
AgenteIA/           Clases base de agente, entorno y busqueda
Rio.py              Interfaz PyGame e integracion de asistencia
main.py             Punto de entrada
Bote.py             Representacion de la barca
Personaje.py        Representacion de los personajes
imagenes/           Recursos graficos
sonido/             Musica y efectos de sonido
material/           Guia de la practica
test_agente_mapu.py Pruebas unitarias
requirements.txt    Dependencias externas
```
