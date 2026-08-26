from AgenteIA.AgenteBuscador import AgenteBuscador
import time


class AgenteMapu(AgenteBuscador):

    def __init__(self):
        AgenteBuscador.__init__(self)
        self.rendimiento = {}
        self.acciones = []

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

    def obtener_instruccion(self, estado, siguiente, numero_paso):
        pacificos = abs(estado[0] - siguiente[0])
        verdugos = abs(estado[1] - siguiente[1])
        direccion = "derecha" if estado[2] == 1 else "izquierda"
        tripulacion = self.describir_tripulacion(pacificos, verdugos)
        return f"Paso {numero_paso}: lleva {tripulacion} a la {direccion}."


    def programa(self):
        inicio = self.get_estado_inicial()
        meta = self.get_estado_meta()
        frontera = [[inicio]]
        visitados = {tuple(inicio)}
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
        self.rendimiento = {
            "tiempo": tiempo,
            "espacio_maximo": espacio_maximo,
            "profundidad": len(camino) - 1 if camino else 0,
            "nodos_expandidos": nodos_expandidos,
        }

        if camino is None:
            self.acciones = ["No encontre una solucion valida para este estado."]
            self.set_acciones(self.acciones)
            return

        instrucciones = [
            "He utilizado busqueda en amplitud: primero reviso las soluciones mas cortas.",
            "Las reglas se respetan en las dos orillas: los verdugos nunca superan a los aldeanos cuando hay aldeanos.",
        ]
        instrucciones.extend(
            self.obtener_instruccion(camino[i], camino[i + 1], i + 1)
            for i in range(len(camino) - 1)
        )
        instrucciones.append(
            f"Solucion completada en {self.rendimiento['profundidad']} movimientos."
        )
        instrucciones.append(
            f"Rendimiento: {self.rendimiento['nodos_expandidos']} nodos explorados, "
            f"frontera maxima de {self.rendimiento['espacio_maximo']} estados y "
            f"{self.rendimiento['tiempo']:.6f} segundos."
        )
        self.acciones = instrucciones
        self.set_acciones(instrucciones)
