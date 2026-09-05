from AgenteIA.AgenteBuscador import AgenteBuscador
import time


class AgenteMapu(AgenteBuscador):

    def __init__(self):
        AgenteBuscador.__init__(self)
        self.rendimiento = {}
        self.rendimiento_busqueda = {}
        self.rendimiento_comparativo = {}
        self.acciones = []
        self._camino_actual = []
        self.algoritmo_actual = "bfs"
        self._comparacion_activa = {}
        self.reiniciar_rendimiento_partida()

    def reiniciar_rendimiento_partida(self):
        self.rendimiento = {
            "tiempo": 0.0,
            "espacio_maximo": 0,
            "profundidad": 0,
            "nodos_expandidos": 0,
            "movimientos": 0,
        }
        self.rendimiento_busqueda = {}
        self.rendimiento_comparativo = {}
        self._camino_actual = []
        self._comparacion_activa = {}

    def registrar_movimiento(self):
        self.rendimiento["movimientos"] += 1

    def obtener_mensaje_rendimiento_global(self, algoritmo=None, comparacion=None):
        algoritmo = (algoritmo or self.algoritmo_actual or "bfs").lower()
        nombre = "BFS" if algoritmo == "bfs" else "DFS"
        ruta_actual = self._camino_actual if self._camino_actual else []
        longitud = max(len(ruta_actual) - 1, self.rendimiento_busqueda.get("profundidad", 0))
        lines = [
            f"Solucion completada en {self.rendimiento['movimientos']} movimientos.",
            f"Rendimiento {nombre}: {self.rendimiento['nodos_expandidos']} nodos explorados, "
            f"frontera maxima de {self.rendimiento['espacio_maximo']} estados y "
            f"{self.rendimiento['tiempo']:.6f} segundos.",
            f"Longitud de la solucion {nombre}: {longitud} movimientos.",
        ]
        if comparacion:
            nombre_otro = "DFS" if algoritmo == "bfs" else "BFS"
            lines.append(
                f"Comparacion con {nombre_otro}: {comparacion.get('texto', '')}"
            )
        return lines

    def obtener_mensaje_rendimiento_algoritmo(self, algoritmo=None):
        algoritmo = (algoritmo or self.algoritmo_actual or "bfs").lower()
        nombre = "BFS" if algoritmo == "bfs" else "DFS"
        if not self.rendimiento_busqueda:
            return [f"Algoritmo activo: {nombre}.", "No hay datos de rendimiento disponibles."]
        return [
            f"Algoritmo activo: {nombre}.",
            f"Longitud: {self.rendimiento_busqueda['profundidad']} movimientos.",
            f"Nodos explorados: {self.rendimiento_busqueda['nodos_expandidos']}.",
            f"Tiempo: {self.rendimiento_busqueda['tiempo']:.6f} segundos.",
            f"Frontera maxima: {self.rendimiento_busqueda['espacio_maximo']} estados.",
        ]

    def generar_reporte_metricas(self, camino_bfs=None, camino_dfs=None, algoritmo_activo=None):
        if camino_bfs is not None and camino_dfs is not None:
            bfs_camino = camino_bfs
            dfs_camino = camino_dfs
        else:
            bfs_camino = self.buscar_solucion("bfs")
            dfs_camino = self.buscar_solucion("dfs")

        bfs_metricas = self._resolver_algoritmo("bfs", self.get_estado_inicial(), self.get_estado_meta())[1]
        dfs_metricas = self._resolver_algoritmo("dfs", self.get_estado_inicial(), self.get_estado_meta())[1]
        texto = (
            f"BFS: longitud={len(bfs_camino) - 1}, nodos explorados={bfs_metricas['nodos_expandidos']}, "
            f"tiempo={bfs_metricas['tiempo']:.6f}s, frontera maxima={bfs_metricas['espacio_maximo']}.\n"
            f"DFS: longitud={len(dfs_camino) - 1}, nodos explorados={dfs_metricas['nodos_expandidos']}, "
            f"tiempo={dfs_metricas['tiempo']:.6f}s, frontera maxima={dfs_metricas['espacio_maximo']}."
        )
        self.rendimiento_comparativo = {
            "bfs": bfs_metricas,
            "dfs": dfs_metricas,
            "texto": texto,
        }
        return texto

    def buscar_solucion(self, algoritmo="bfs", estado=None, meta=None):
        estado = list(estado if estado is not None else self.get_estado_inicial())
        meta = list(meta if meta is not None else self.get_estado_meta())
        camino, _ = self._resolver_algoritmo(algoritmo=algoritmo, estado=estado, meta=meta)
        return camino

    def _resolver_algoritmo(self, algoritmo="bfs", estado=None, meta=None):
        estado = list(estado if estado is not None else self.get_estado_inicial())
        meta = list(meta if meta is not None else self.get_estado_meta())
        algoritmo = (algoritmo or "bfs").lower()
        if algoritmo == "bfs":
            return self._buscar_bfs(estado, meta)
        if algoritmo == "dfs":
            return self._buscar_dfs(estado, meta)
        raise ValueError(f"Algoritmo no soportado: {algoritmo}")

    def _buscar_bfs(self, estado, meta):
        frontera = [[list(estado)]]
        visitados = {tuple(estado)}
        nodos_expandidos = 0
        espacio_maximo = len(frontera)
        camino = None
        tiempo_inicio = time.perf_counter()

        while frontera:
            camino_actual = frontera.pop(0)
            nodo = camino_actual[-1]
            nodos_expandidos += 1

            if nodo == meta:
                camino = camino_actual
                break

            for _, _, hijo in self.pasa_aa(nodo):
                clave_hijo = tuple(hijo)
                if clave_hijo not in visitados:
                    visitados.add(clave_hijo)
                    frontera.append(camino_actual + [hijo])

            espacio_maximo = max(espacio_maximo, len(frontera))

        tiempo = time.perf_counter() - tiempo_inicio
        metricas = {
            "tiempo": tiempo,
            "espacio_maximo": espacio_maximo,
            "profundidad": len(camino) - 1 if camino else 0,
            "nodos_expandidos": nodos_expandidos,
        }
        return camino, metricas

    def _buscar_dfs(self, estado, meta):
        pila = [[list(estado)]]
        visitados = {tuple(estado)}
        nodos_expandidos = 0
        espacio_maximo = len(pila)
        camino = None
        tiempo_inicio = time.perf_counter()

        while pila:
            camino_actual = pila.pop()
            nodo = camino_actual[-1]
            nodos_expandidos += 1

            if nodo == meta:
                camino = camino_actual
                break

            for _, _, hijo in reversed(self.pasa_aa(nodo)):
                clave_hijo = tuple(hijo)
                if clave_hijo not in visitados:
                    visitados.add(clave_hijo)
                    pila.append(camino_actual + [hijo])

            espacio_maximo = max(espacio_maximo, len(pila))

        tiempo = time.perf_counter() - tiempo_inicio
        metricas = {
            "tiempo": tiempo,
            "espacio_maximo": espacio_maximo,
            "profundidad": len(camino) - 1 if camino else 0,
            "nodos_expandidos": nodos_expandidos,
        }
        return camino, metricas

    def pasa_aa(self, e):
        """Genera los estados validos alcanzables desde e.

        Un estado es [pacificos_izquierda, verdugos_izquierda, bote_izquierda].
        Cada sucesor conserva tambien la tripulacion que produjo el movimiento.
        """
        pacificos, verdugos, bote_izquierda = e
        pacificos_derecha = 3 - pacificos
        verdugos_derecha = 3 - verdugos
        sucesores = []
        tripulaciones = ((1, 0), (2, 0), (0, 1), (0, 2), (1, 1))

        for pacificos_mover, verdugos_mover in tripulaciones:
            if bote_izquierda == 1:
                if pacificos_mover > pacificos or verdugos_mover > verdugos:
                    continue
                nuevo_estado = [
                    pacificos - pacificos_mover,
                    verdugos - verdugos_mover,
                    0,
                ]
            else:
                if pacificos_mover > pacificos_derecha or verdugos_mover > verdugos_derecha:
                    continue
                nuevo_estado = [
                    pacificos + pacificos_mover,
                    verdugos + verdugos_mover,
                    1,
                ]

            if self.es_estado_valido(nuevo_estado):
                sucesores.append((pacificos_mover, verdugos_mover, nuevo_estado))

        return sucesores

    @staticmethod
    def es_estado_valido(estado):
        pacificos, verdugos, _ = estado
        pacificos_derecha = 3 - pacificos
        verdugos_derecha = 3 - verdugos
        izquierda_valida = pacificos == 0 or pacificos >= verdugos
        derecha_valida = pacificos_derecha == 0 or pacificos_derecha >= verdugos_derecha
        return izquierda_valida and derecha_valida

    @staticmethod
    def describir_tripulacion(pacificos, verdugos):
        partes = []
        if pacificos:
            partes.append(f"{pacificos} aldeano" + ("s" if pacificos != 1 else ""))
        if verdugos:
            partes.append(f"{verdugos} verdugo" + ("s" if verdugos != 1 else ""))
        return " y ".join(partes)

    def obtener_instruccion(self, estado, siguiente, numero_paso=None):
        pacificos = abs(estado[0] - siguiente[0])
        verdugos = abs(estado[1] - siguiente[1])
        direccion = "derecha" if estado[2] == 1 else "izquierda"
        tripulacion = self.describir_tripulacion(pacificos, verdugos)
        instruccion = f"Lleva {tripulacion} a la {direccion}."
        if numero_paso is not None:
            instruccion = f"Paso {numero_paso}: {instruccion}"
        return instruccion

    def obtener_pasos_asistencia(self, estado, algoritmo=None, ruta=None):
        algoritmo = (algoritmo or self.algoritmo_actual or "bfs").lower()
        self.algoritmo_actual = algoritmo
        self.set_estado_inicial(list(estado))
        self.set_estado_meta([0, 0, 0])
        if ruta is None:
            camino, metricas = self._resolver_algoritmo(
                algoritmo=algoritmo, estado=list(estado), meta=[0, 0, 0]
            )
            self.rendimiento_busqueda = metricas
            self._camino_actual = camino or []
            self.rendimiento["tiempo"] += metricas["tiempo"]
            self.rendimiento["espacio_maximo"] = max(
                self.rendimiento["espacio_maximo"], metricas["espacio_maximo"]
            )
            self.rendimiento["nodos_expandidos"] += metricas["nodos_expandidos"]
            self.rendimiento["profundidad"] = metricas["profundidad"]
            ruta = camino or []
            if camino is not None:
                nombre_algoritmo = "amplitud" if algoritmo == "bfs" else "profundidad"
                self.acciones = [
                    (
                        f"He utilizado busqueda en {nombre_algoritmo}: reviso primero las soluciones mas cortas."
                        if algoritmo == "bfs"
                        else "He utilizado busqueda en profundidad: exploro un camino hasta el final antes de retroceder."
                    ),
                    "Las reglas se respetan en las dos orillas: los verdugos nunca superan a los aldeanos cuando hay aldeanos.",
                ]
                self.set_acciones(self.acciones)
        else:
            self._camino_actual = [list(nodo) for nodo in ruta]
        if not ruta:
            return []
        return [
            self.obtener_instruccion(estado_actual, siguiente)
            for estado_actual, siguiente in zip(ruta[:-1], ruta[1:])
        ]

    def programa(self, algoritmo="bfs"):
        algoritmo = (algoritmo or "bfs").lower()
        self.algoritmo_actual = algoritmo
        inicio = self.get_estado_inicial()
        meta = self.get_estado_meta()
        camino, metricas = self._resolver_algoritmo(algoritmo=algoritmo, estado=inicio, meta=meta)
        self.rendimiento_busqueda = metricas
        self.rendimiento["tiempo"] += metricas["tiempo"]
        self.rendimiento["espacio_maximo"] = max(
            self.rendimiento["espacio_maximo"], metricas["espacio_maximo"]
        )
        self.rendimiento["nodos_expandidos"] += metricas["nodos_expandidos"]

        if camino is None:
            self._camino_actual = []
            self.acciones = ["No encontre una solucion valida para este estado."]
            self.set_acciones(self.acciones)
            return

        self._camino_actual = camino
        nombre_algoritmo = "amplitud" if algoritmo == "bfs" else "profundidad"
        instrucciones = [
            f"He utilizado busqueda en {nombre_algoritmo}: reviso primero las soluciones mas cortas." if algoritmo == "bfs" else "He utilizado busqueda en profundidad: exploro un camino hasta el final antes de retroceder.",
            "Las reglas se respetan en las dos orillas: los verdugos nunca superan a los aldeanos cuando hay aldeanos.",
        ]
        instrucciones.extend(
            self.obtener_instruccion(camino[i], camino[i + 1], i + 1)
            for i in range(len(camino) - 1)
        )
        instrucciones.append(
            f"Solucion parcial encontrada en {self.rendimiento_busqueda['profundidad']} movimientos."
        )
        instrucciones.append(
            f"Busqueda parcial: {self.rendimiento_busqueda['nodos_expandidos']} nodos explorados, "
            f"frontera maxima de {self.rendimiento_busqueda['espacio_maximo']} estados y "
            f"{self.rendimiento_busqueda['tiempo']:.6f} segundos."
        )
        self.acciones = instrucciones
        self.set_acciones(instrucciones)
