# Village Savior Agent

Agente inteligente para resolver el problema del cruce del rio de los aldeanos y verdugos. El proyecto utiliza Python, Pygame y Pyttsx4 para combinar busqueda en espacios de estados, interfaz grafica e instrucciones por voz.

## Objetivo

El agente debe transportar a tres aldeanos y tres verdugos desde la orilla izquierda hasta la derecha. En cada viaje el bote puede llevar uno o dos personajes. Los verdugos no pueden superar en numero a los aldeanos en una orilla cuando hay aldeanos presentes.

La representacion de cada estado es:

```text
[aldeanos_en_la_izquierda, verdugos_en_la_izquierda, bote_en_la_izquierda]
```

- `bote_en_la_izquierda = 1`: el bote esta en la izquierda.
- `bote_en_la_izquierda = 0`: el bote esta en la derecha.
- Estado inicial: `[3, 3, 1]`.
- Estado meta: `[0, 0, 0]`.

## Metodologia de la fase 2

La implementacion se baso en los notebooks de la practica:

1. `02_agentes.ipynb` presenta las abstracciones `Agente` y `Entorno`, junto con el ciclo de percepcion y ejecucion.
2. `03_agente_buscador.ipynb` introduce estados iniciales, estados meta, funciones sucesor y fronteras de caminos.
3. `03-busqueda_no_inf.ipynb` explica la busqueda no informada y aplica amplitud al problema de los aldeanos y verdugos.

Se decidio mantener la estructura proporcionada del proyecto. Por ello, la solucion se implemento exclusivamente en `AgenteMapu.py`, conservando la compatibilidad con `AgenteBuscador`, `Entorno` y la interfaz grafica existente.

## Cambios en `AgenteMapu.py`

### Generacion de sucesores

El metodo `pasa_aa(estado)` prueba las cinco tripulaciones permitidas:

- Un aldeano.
- Dos aldeanos.
- Un verdugo.
- Dos verdugos.
- Un aldeano y un verdugo.

Para cada alternativa comprueba que haya suficientes personajes en la orilla de salida, mueve el bote a la orilla opuesta y conserva solo los estados validos.

### Validacion del problema

`es_estado_valido(estado)` calcula la cantidad de personajes en ambas orillas. Un estado se acepta cuando:

- Los aldeanos y verdugos estan dentro del rango valido.
- En cada orilla los verdugos no superan a los aldeanos, excepto cuando no hay aldeanos en esa orilla.

### Busqueda en amplitud

`programa()` implementa busqueda en amplitud usando una frontera FIFO. Cada elemento de la frontera es un camino completo de estados. El algoritmo:

1. Comienza con el estado inicial.
2. Extrae primero el camino mas antiguo.
3. Comprueba si su ultimo estado es la meta.
4. Genera sus sucesores validos.
5. Agrega a la frontera los estados que aun no fueron visitados.

Como todos los viajes tienen el mismo costo, amplitud encuentra una solucion con el menor numero de movimientos. Para el estado inicial de la practica, la solucion encontrada tiene 11 movimientos.

### Instrucciones educativas

El agente transforma el camino de estados en mensajes claros en espanol, por ejemplo:

```text
Paso 1: lleva 2 aldeanos a la derecha.
```

Tambien informa que se utilizo busqueda en amplitud, recuerda la restriccion principal y comunica el resultado final. Estas frases se guardan en `acciones`, que es el atributo que consume la interfaz del juego.

### Metricas de rendimiento

El agente registra en `rendimiento`:

- `tiempo`: suma de los segundos empleados en todas las busquedas BFS.
- `espacio_maximo`: mayor cantidad de caminos almacenados en la frontera entre todas las busquedas.
- `nodos_expandidos`: suma de los estados examinados en todas las busquedas.
- `movimientos`: cantidad de cruces completados por el jugador.
- `profundidad`: profundidad de la busqueda mas reciente; se conserva como dato interno y no se muestra como metrica final.

Las metricas globales solo se incluyen en el mensaje final, cuando el jugador llega a `[0, 0, 0]`. Las metricas de cada busqueda parcial se conservan internamente para acumularlas, pero no se imprimen ni se leen durante los pasos. El resumen final se imprime en la terminal y Pyttsx4 lo lee mediante voz; la ventana grafica muestra el estado del juego, pero no contiene un panel visual separado para estas metricas.

### Como presentar los resultados de rendimiento

Para obtener los resultados desde la terminal, ejecuta el juego desde la raiz del proyecto:

```powershell
python main.py
```

Con el juego abierto, pulsa el boton de asistencia. El agente calculara la primera solucion. Cada vez que completes un cruce, puede recalcular el siguiente tramo desde el estado actual, pero esas metricas parciales no se muestran. Al completar la partida, `Rio.py` imprimira el resumen global en la terminal. La salida tiene esta forma:

```text
Solucion completada en 11 movimientos.
Rendimiento global: 45 nodos explorados, frontera maxima de 3 estados y 0.000250 segundos.
```

Tambien se pueden consultar directamente todas las metricas sin abrir la ventana grafica:

```powershell
python -c "from AgenteMapu import AgenteMapu; a=AgenteMapu(); a.set_estado_inicial([3,3,1]); a.set_estado_meta([0,0,0]); a.programa(); print(a.rendimiento)"
```

Para el informe tecnico, organiza los valores en una tabla como esta:

| Metrica | Resultado |
|---|---:|
| Tiempo | 0.000031 segundos |
| Espacio maximo | 3 estados |
| Movimientos realizados | 11 |
| Nodos expandidos acumulados | 45 |

El tiempo y los nodos acumulados dependen de las decisiones del jugador: una ruta alternativa puede provocar busquedas parciales diferentes. Para un analisis mas confiable, ejecuta varias partidas y presenta el promedio del tiempo junto con los movimientos, el espacio maximo y los nodos acumulados.

## Pruebas unitarias de la funcion sucesor

Las pruebas de la fase 5 estan en `test_agente_mapu.py` y utilizan `unittest`, una biblioteca incluida en Python. Por lo tanto, no es necesario instalar otra dependencia para ejecutarlas.

### Como ejecutar las pruebas

Abre una terminal en la raiz del proyecto, es decir, en la carpeta que contiene `AgenteMapu.py`, y ejecuta:

```powershell
python -m unittest -v test_agente_mapu.py
```

La opcion `-v` muestra el nombre y el resultado de cada prueba. Para ejecutar todas las pruebas Python que sigan el patron habitual tambien se puede usar:

```powershell
python -m unittest discover -v
```

### Que devuelve `pasa_aa()`

La funcion recibe un estado con la forma `[aldeanos_izquierda, verdugos_izquierda, bote_izquierda]`. Devuelve una lista de tuplas con esta forma:

```text
(aldeanos_movidos, verdugos_movidos, nuevo_estado)
```

Las pruebas convierten `nuevo_estado` en una tupla unicamente para poder comparar conjuntos de resultados. La implementacion sigue devolviendo listas, como espera el agente.

### Que verifica cada prueba

- `test_genera_todos_los_sucesores_validos_del_estado_inicial`: comprueba que desde `[3, 3, 1]` se generen exactamente los tres movimientos validos. Esto evita que falten alternativas o se acepten movimientos imposibles.
- `test_genera_movimientos_desde_la_orilla_derecha`: comprueba el caso contrario, cuando el bote esta en la derecha. Asi se verifica que el calculo de personajes disponibles y el sentido del viaje funcionen en ambas orillas.
- `test_los_sucesores_son_estados_validos`: pasa varios estados al agente y confirma que cada sucesor respete la regla de los aldeanos y verdugos.
- `test_el_bote_cambia_de_orilla_y_transporta_uno_o_dos_personajes`: verifica dos reglas mecanicas: el bote siempre cambia de orilla y nunca transporta cero ni mas de dos personajes.
- `test_no_modifica_el_estado_recibido`: conserva una copia del estado original y comprueba que `pasa_aa()` no lo altere mientras genera los sucesores.

Las pruebas combinan comparaciones exactas, aserciones booleanas, comprobacion de valores permitidos y subpruebas por estado. Esto permite detectar tanto resultados faltantes o sobrantes como errores en las restricciones o efectos secundarios.

### Como interpretar los resultados

Una ejecucion correcta termina con una salida similar a:

```text
Ran 5 tests in 0.001s

OK
```

`OK` significa que las cinco pruebas pasaron y que la funcion sucesor cumple los casos cubiertos. Cada linea terminada en `ok` confirma una prueba individual.

Si aparece `FAIL`, una asercion no coincide con el resultado esperado. El informe muestra el nombre de la prueba y los elementos que faltan o sobran; normalmente indica un error en la generacion de sucesores, en la validacion de estados o en el sentido del bote.

Si aparece `ERROR`, la prueba no pudo ejecutarse por una excepcion, por ejemplo un import incorrecto o un error de estructura en el codigo. En ese caso se debe revisar el traceback mostrado antes del resumen.

Estas pruebas validan directamente `pasa_aa()` y no reemplazan la prueba manual del juego grafico ni la medicion de la busqueda en amplitud. Su objetivo es detectar rapidamente regresiones en la funcion sucesor antes de ejecutar la aplicacion completa.

## Mejoras creativas de la fase 3

Las mejoras creativas se implementaron unicamente dentro de `AgenteMapu.py`, sin agregar archivos, imagenes ni modulos nuevos. Se eligio una mejora educativa porque el proyecto esta pensado para ayudar a comprender la planificacion y la busqueda:

- El agente explica que utiliza busqueda en amplitud y que esta estrategia revisa primero las soluciones mas cortas.
- Recuerda la regla principal: los verdugos no pueden superar a los aldeanos cuando hay aldeanos en la orilla.
- Convierte cada transicion del camino en una instruccion numerada y comprensible, como `Paso 1: lleva 2 aldeanos a la derecha.`
- Informa cuando la solucion fue completada y cuantos movimientos necesito.
- Comunica el tiempo, el espacio maximo de la frontera y los nodos explorados como parte del resumen de asistencia.
- Usa el mismo texto para la salida de la terminal y para la lectura por voz, de modo que la mejora sea accesible durante la partida.

Estas funcionalidades se activan al pulsar el boton de asistencia. Mejoran la experiencia sin alterar la logica de movimiento manual del jugador.

## Actualizaciones recientes

Las siguientes funcionalidades, mejoras y correcciones se agregaron despues de la implementacion inicial del agente:

### Asistencia interactiva

- La asistencia comienza leyendo las dos explicaciones generales sobre busqueda en amplitud y las restricciones del problema.
- Despues muestra junto a la imagen del agente un cuadro de dialogo con una sola instruccion vigente.
- Los pasos del dialogo no llevan numeracion para que puedan cambiar sin confundir al jugador.
- El siguiente dialogo aparece unicamente cuando el jugador completa un cruce y el estado del juego cambia.
- Si el jugador sigue el estado sugerido, el agente reutiliza el camino guardado y no ejecuta otra busqueda.
- Si el jugador toma otra alternativa valida, el agente ejecuta una nueva busqueda en amplitud desde ese estado y muestra la siguiente instruccion valida.
- Al alcanzar el estado meta, desaparece el dialogo de pasos y se leen solamente las dos lineas finales con el resultado y las metricas globales.

### Correcciones de interfaz y audio

- La voz se reproduce en un hilo separado, por lo que `runAndWait()` ya no bloquea la ventana de Pygame.
- El boton `AGENTE` se procesa mediante un evento unico `MOUSEBUTTONDOWN`; un solo clic no vuelve a ejecutar la asistencia varias veces.
- Se evita iniciar varias locuciones simultaneas si el jugador pulsa el boton mientras una asistencia sigue reproduciendose.
- Ya no se fuerza el identificador literal `spanish`, que no existe en todas las instalaciones. Se busca una voz española disponible y, si no se encuentra, se conserva la voz predeterminada.
- El volumen de la musica y de los efectos del juego se fija al 70% de su nivel de referencia.
- El volumen de la voz aumenta un 35% respecto a su valor actual, con un limite maximo del 100% permitido por el motor.

### Metricas globales de la partida

La primera busqueda calcula y conserva el camino completo sugerido. Mientras el jugador siga ese camino, no se ejecutan nuevas BFS. Solo se realiza una busqueda parcial adicional cuando el jugador completa un cruce valido hacia un estado distinto al estado sugerido. No se muestran los resultados individuales de esas busquedas. Al completar la partida se presenta un unico resumen global con:

- Todos los cruces realizados por el jugador.
- La suma del tiempo empleado por todas las busquedas BFS ejecutadas.
- La suma de los nodos explorados en todas las busquedas ejecutadas.
- El mayor tamaño de frontera alcanzado durante cualquier busqueda.

Esto permite que una ruta alternativa se refleje correctamente en el resultado final. Si el jugador sigue la primera solucion sin desviarse, las metricas globales corresponden a una sola BFS; si se desvía, se suman unicamente los nodos y el tiempo de las nuevas BFS ejecutadas.

- `test_agente_mapu.py` contiene cinco pruebas unitarias para `pasa_aa()`.
- `README.md` documenta la solucion, las pruebas, la asistencia interactiva, las correcciones de audio y la interpretacion de las metricas.
- Los cambios de esta etapa se concentran en `AgenteMapu.py`, `Rio.py` y `README.md`; no se agregaron recursos graficos ni archivos de configuracion adicionales.

## Cambios visibles en el juego

La integracion se realiza en `Rio.py`, mientras que la logica del agente permanece en `AgenteMapu.py`. Al pulsar el boton de asistencia de la interfaz:

- Se ejecuta el agente buscador.
- Se muestran por consola las instrucciones generadas.
- Pygame las entrega al motor de voz de Pyttsx4.
- El jugador recibe la secuencia de movimientos y el resumen de rendimiento.
- La reproduccion de voz se ejecuta en un hilo separado para que la ventana no deje de responder.
- Se busca una voz española instalada mediante su identificador; si no existe, se usa la voz predeterminada.
- El boton `AGENTE` se procesa como un evento unico de clic, evitando imprimir o iniciar varias veces la misma asistencia mientras el boton permanece presionado.

La interfaz, los personajes, las imagenes y los sonidos existentes se conservan sin cambios.

## Instalacion

Se necesita Python 3.10 o una version posterior instalado en el equipo y agregado al `PATH` de Windows.

Desde la raiz del proyecto, instala las dependencias con:

```powershell
python -m pip install -r requirements.txt
```

Las dependencias externas son:

- `pygame`: ventana, graficos, interaccion y reproduccion de sonidos.
- `pyttsx4`: instrucciones de asistencia mediante voz.

## Ejecucion

Abre una terminal en la carpeta que contiene `main.py` y ejecuta:

```powershell
python main.py
```

Es importante ejecutar el comando desde la raiz del proyecto porque el juego carga sus recursos usando las rutas relativas `imagenes/` y `sonido/`.

En la ventana del juego, utiliza el boton de asistencia para solicitar la solucion del agente. El boton de sonido permite activar o desactivar el audio.

## Estructura principal

```text
AgenteMapu.py       Agente solucionador del problema
AgenteIA/           Clases base de agente, entorno y busqueda
Rio.py              Entorno grafico e integracion de asistencia
Bote.py             Representacion del bote
Personaje.py        Representacion de los personajes
main.py             Punto de entrada del juego
imagenes/           Recursos graficos
sonido/             Musica y efectos de sonido
material/           Notebooks y guia de la practica
requirements.txt    Dependencias de Python
```

## Control de versiones

El archivo `.gitignore` excluye configuraciones locales de IDE, archivos compilados de Python, entornos virtuales, logs y archivos temporales. El codigo fuente, los recursos del juego y el material academico se mantienen versionados.
