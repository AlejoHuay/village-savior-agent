import unittest

from AgenteMapu import AgenteMapu


def obtener_rutas_validas(agente, estado, meta, camino=None):
    camino = camino or [tuple(estado)]
    if tuple(estado) == tuple(meta):
        return [camino]

    rutas = []
    for _, _, sucesor in agente.pasa_aa(list(estado)):
        siguiente = tuple(sucesor)
        if siguiente not in camino:
            rutas.extend(obtener_rutas_validas(agente, siguiente, meta, camino + [siguiente]))
    return rutas


class TestPasaAa(unittest.TestCase):

    def setUp(self):
        self.agente = AgenteMapu()

    def test_genera_todos_los_sucesores_validos_del_estado_inicial(self):
        sucesores = self.agente.pasa_aa([3, 3, 1])

        resultados = {
            (pacificos, verdugos, tuple(estado))
            for pacificos, verdugos, estado in sucesores
        }
        esperados = {
            (0, 1, (3, 2, 0)),
            (0, 2, (3, 1, 0)),
            (1, 1, (2, 2, 0)),
        }

        self.assertEqual(resultados, esperados)

    def test_genera_movimientos_desde_la_orilla_derecha(self):
        sucesores = self.agente.pasa_aa([0, 2, 0])

        resultados = {
            (pacificos, verdugos, tuple(estado))
            for pacificos, verdugos, estado in sucesores
        }

        self.assertEqual(
            resultados,
            {
                (2, 0, (2, 2, 1)),
                (0, 1, (0, 3, 1)),
            },
        )

    def test_los_sucesores_son_estados_validos(self):
        estados = (
            [3, 3, 1],
            [3, 1, 0],
            [2, 2, 0],
            [1, 2, 1],
            [0, 0, 0],
        )

        for estado in estados:
            with self.subTest(estado=estado):
                for _, _, sucesor in self.agente.pasa_aa(estado):
                    self.assertTrue(self.agente.es_estado_valido(sucesor))

    def test_el_bote_cambia_de_orilla_y_transporta_uno_o_dos_personajes(self):
        for estado in ([3, 3, 1], [0, 2, 0]):
            with self.subTest(estado=estado):
                for pacificos, verdugos, sucesor in self.agente.pasa_aa(estado):
                    self.assertEqual(sucesor[2], 1 - estado[2])
                    self.assertIn(pacificos + verdugos, (1, 2))

    def test_no_modifica_el_estado_recibido(self):
        estado = [3, 3, 1]
        copia = estado[:]

        self.agente.pasa_aa(estado)

        self.assertEqual(estado, copia)


class TestEscenariosAsistencia(unittest.TestCase):

    def setUp(self):
        self.agente = AgenteMapu()
        self.inicio = (3, 3, 1)
        self.meta = (0, 0, 0)
        self.rutas = obtener_rutas_validas(self.agente, self.inicio, self.meta)

    def test_todas_las_soluciones_validas_pueden_recalcularse(self):
        self.assertEqual(len(self.rutas), 4)

        for ruta in self.rutas:
            with self.subTest(ruta=ruta):
                for estado in ruta[:-1]:
                    pasos = self.agente.obtener_pasos_asistencia(list(estado))
                    self.assertTrue(pasos)
                    self.assertEqual(tuple(self.agente._camino_actual[0]), estado)
                    self.assertEqual(tuple(self.agente._camino_actual[-1]), self.meta)
                    self.assertTrue(
                        all(self.agente.es_estado_valido(nodo) for nodo in self.agente._camino_actual)
                    )

    def test_varios_cambios_de_ruta_validos_acumulan_bfs(self):
        estados_alternativos = [
            self.rutas[1][1],
            self.rutas[2][3],
            self.rutas[3][5],
        ]
        self.agente.reiniciar_rendimiento_partida()
        nodos_esperados = 0

        for estado in [self.inicio] + estados_alternativos:
            pasos = self.agente.obtener_pasos_asistencia(list(estado))
            self.assertTrue(pasos)
            nodos_esperados += self.agente.rendimiento_busqueda["nodos_expandidos"]
            self.assertEqual(tuple(self.agente._camino_actual[0]), estado)
            self.assertEqual(tuple(self.agente._camino_actual[-1]), self.meta)

        self.assertEqual(self.agente.rendimiento["movimientos"], 0)
        self.assertEqual(self.agente.rendimiento["nodos_expandidos"], nodos_esperados)
        self.assertGreater(self.agente.rendimiento["tiempo"], 0)

    def test_recalcular_despues_de_varias_decisiones_no_corrompe_el_agente(self):
        estados = [list(self.inicio)]
        for ruta in self.rutas:
            estados.extend(list(estado) for estado in ruta[1:4])

        self.agente.reiniciar_rendimiento_partida()
        for estado in estados:
            pasos = self.agente.obtener_pasos_asistencia(estado)
            self.assertTrue(pasos)
            self.assertTrue(self.agente.es_estado_valido(self.agente._camino_actual[0]))
            self.assertEqual(tuple(self.agente._camino_actual[-1]), self.meta)

        self.assertEqual(self.agente.rendimiento["movimientos"], 0)
        self.assertGreater(self.agente.rendimiento["nodos_expandidos"], 15)


if __name__ == "__main__":
    unittest.main()
