import unittest

from AgenteMapu import AgenteMapu


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


if __name__ == "__main__":
    unittest.main()
