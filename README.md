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

- `tiempo`: segundos empleados en encontrar la solucion.
- `espacio_maximo`: mayor cantidad de caminos almacenados en la frontera.
- `profundidad`: numero de movimientos de la solucion.
- `nodos_expandidos`: cantidad de estados examinados.

Estas metricas se incluyen tambien en el mensaje final de asistencia para que puedan observarse desde el juego.

## Cambios visibles en el juego

No se modificaron `Rio.py` ni los demas archivos base. Al pulsar el boton de asistencia de la interfaz:

- Se ejecuta el agente buscador.
- Se muestran por consola las instrucciones generadas.
- Pygame las entrega al motor de voz de Pyttsx4.
- El jugador recibe la secuencia de movimientos y el resumen de rendimiento.

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
