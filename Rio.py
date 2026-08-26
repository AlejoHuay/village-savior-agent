from AgenteIA.Entorno import Entorno
import pygame
import pyttsx4
from Bote import Bote
from Personaje import Personaje


class Rio(Entorno):
    def __init__(self):
        Entorno.__init__(self)
        # incializar pygame
        pygame.init()
        self.habla = pyttsx4.init()
        self.habla.setProperty('voice', "spanish")
        self.habla.setProperty('rate', 150)

    def get_percepciones(self, agente):
        agente.programa()

    def ejecutar(self, agente):
        # definimos la ventana principal
        ancho = 1280
        altura = 650
        ventana = pygame.display.set_mode((ancho, altura))
        pygame.display.set_caption('Inteligencia Artificial I')

        negro = (0, 0, 0)

        # cargamos imagenes
        agente_img = pygame.image.load('imagenes/agente.png')
        bote_img = pygame.image.load('imagenes/bote.png')
        fondo_img = pygame.image.load('imagenes/fondo.png')
        pacifico_img = pygame.image.load('imagenes/pacifico.png')
        pacifico1_img = pygame.image.load('imagenes/pacifico1.png')
        verdugo_img = pygame.image.load('imagenes/verdugo.png')
        verdugo1_img = pygame.image.load('imagenes/verdugo1.png')
        nuevo_img = pygame.image.load('imagenes/nuevo.png')
        nuevo1_img = pygame.image.load('imagenes/nuevo1.png')
        agente_btn_img = pygame.image.load('imagenes/agente_btn.png')
        agente_btn1_img = pygame.image.load('imagenes/agente_btn1.png')
        fin_img = pygame.image.load('imagenes/fin.png')
        victoria_img = pygame.image.load('imagenes/victoria.png')
        go_img = pygame.image.load('imagenes/go.png')
        go1_img = pygame.image.load('imagenes/go1.png')
        sonido_on_img = pygame.image.load('imagenes/sonidoon.png')
        sonido_off_img = pygame.image.load('imagenes/sonidooff.png')

        # cargamos sonido
        snd_fin = pygame.mixer.Sound('sonido/sonido_fin.wav')
        snd_victoria = pygame.mixer.Sound('sonido/sonido_ganador.wav')

        font = pygame.font.SysFont(None, 25)

        x = (ancho * 0.1)
        y = (altura * 0.8)
        x_nuevo, y_nuevo = 0, 0

        # insertamos los personajes en la orilla izquierda y los colocamos en la esena
        personajes = []
        personajes.insert(0, Personaje(x - 135, y - 100, 0, 0, 'P', 'izquierda', pacifico_img, pacifico1_img, ventana))
        personajes.insert(1, Personaje(x - 90, y - 100, 0, 0, 'P', 'izquierda', pacifico_img, pacifico1_img, ventana))
        personajes.insert(2, Personaje(x - 45, y - 100, 0, 0, 'P', 'izquierda', pacifico_img, pacifico1_img, ventana))
        personajes.insert(3, Personaje(x - 135, y - 250, 0, 0, 'V', 'izquierda', verdugo_img, verdugo1_img, ventana))
        personajes.insert(4, Personaje(x - 90, y - 250, 0, 0, 'V', 'izquierda', verdugo_img, verdugo1_img, ventana))
        personajes.insert(5, Personaje(x - 45, y - 250, 0, 0, 'V', 'izquierda', verdugo_img, verdugo1_img, ventana))

        # posibles tripulantes en el bote
        en_bote = []
        en_bote.insert(0, Bote(157, 478, 2, pacifico1_img, verdugo1_img, ventana))
        en_bote.insert(1, Bote(656, 478, 3, pacifico1_img, verdugo1_img, ventana))
        en_bote.insert(2, Bote(318, 478, 4, pacifico1_img, verdugo1_img, ventana))
        en_bote.insert(3, Bote(817, 478, 5, pacifico1_img, verdugo1_img, ventana))

        clock = pygame.time.Clock()
        finalizado = False
        pos_bote = 0
        a, b = 0, 0

        accion = [a, b]  # numero de verdugos y pacificos a mover
        pafi, verdug, bt = 3, 3, 1  # Indica 3 verdugos, 3 pacificos en orilla izquierda
        # Representacion del estado
        estado = [pafi, verdug, bt]  # indica estado en orilla izquierda (numero de pacificos y verdugos)

        fin_juego = False
        fin_jugador, victoria_jugador = False, False
        izquierda, derecha = False, False
        victoria = False
        num_movida = 0

        # cargar sonido de fondo
        pygame.mixer.music.load('sonido/sonido_fondo.mp3')
        pygame.mixer.music.play(-1)
        sonido = True
        con_agente = False

        while not finalizado:
            # cargar imagenes de inicio
            # imagen de fondo
            ventana.blit(fondo_img, (0, 0))
            # boton para iniciar nuevo juego
            ventana.blit(nuevo_img, (1000, 45))
            # boton para habilitar sonido
            ventana.blit(agente_btn_img, (700, 45))
            # boton para habilitar sonido
            if sonido:
                ventana.blit(sonido_on_img, (1150, 40))
            else:
                ventana.blit(sonido_off_img, (1150, 40))
            # para cada evento del array de eventos capturados de teclado y mouse....
            for evento in pygame.event.get():
                # si apretamos x de la ventana, salimos del juego
                if evento.type == pygame.QUIT:
                    finalizado = True

            # cargar imagenes para los personajes (el vector de personajes)
            for i in range(6):
                personajes[i].mostrar()

            # mostrar estados, acciones, numero de movimientos
            msg_estado = font.render("Estado: " + str(estado), True, negro)
            ventana.blit(msg_estado, [20, 20])

            msg_accion = font.render("Accion: " + str(accion), True, negro)
            ventana.blit(msg_accion, [20, 50])

            msg_movidas = font.render("Movidas: " + str(num_movida), True, negro)
            ventana.blit(msg_movidas, [20, 80])

            if con_agente:
                ventana.blit(agente_img, (200, 40))

            # capturamos las coordenadas del cursor del mouse
            cursor = pygame.mouse.get_pos()

            # click para habilitar y deshabilitar sonido
            # verificamos si el cursor esta en el area del boton sonido
            if 1150 + 50 > cursor[0] > 1150 and 40 + 50 > cursor[1] > 40:
                # si sonido estaba habilitado
                if sonido:
                    # cambiar a boton deshabilitado
                    ventana.blit(sonido_off_img, (1150, 40))
                else:
                    # caso contrario mostrar boton habilitado
                    ventana.blit(sonido_on_img, (1150, 40))
                # si se detecta click izquierdo del mouse
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    if sonido:
                        # cambiamos la bandera sonido, y colocamos pausa a la musica
                        sonido = False
                        pygame.mixer.music.pause()
                    else:
                        # habilitamos la bandera sonido y colocamos play a la musica
                        sonido = True
                        pygame.mixer.music.play()

            # click para nuevo juego
            # verificamos si el cursor esta en el area del boton nuevo
            if 1000 + 119 > cursor[0] > 1000 and 45 + 36 > cursor[1] > 45:
                ventana.blit(nuevo1_img, (1000, 20))
                # si se hace click en el boton nuevo
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    # reiniciamos el entorno rio y a los agentes
                    self.run()

            # click para pedir recomendacion al agente
            # verificamos si el cursor esta en el area del boton agente
            if 700 + 119 > cursor[0] > 700 and 45 + 36 > cursor[1] > 45:
                ventana.blit(agente_btn1_img, (700, 20))
                # si se hace click en el boton nuevo
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    # mostramos a nuestro agente
                    ventana.blit(agente_img, (200, 40))
                    # llamamos a percibir, aqui debemos capturar
                    # el estado en el que se encuentra el problema
                    # para que el programa agente resuelva el problema
                    # dejando la respuesta en el atributo acciones.
                    self.get_percepciones(agente)
                    con_agente = True

            # mostrar bote
            ventana.blit(bote_img, (int(x), int(y)))

            # verificar fin del juego
            if (estado[1] > estado[0] > 0) or (estado[1] < estado[0] < 3):
                ventana.blit(fin_img, (400, 250))
                fin_juego = True

            # verificar victoria
            if estado == [0, 0, 0] and accion == [0, 0]:
                ventana.blit(victoria_img, (400, 250))
                victoria = True

            if not fin_juego and not victoria:
                # verificar boton "GO"
                if 590 + 88 > cursor[0] > 590 and 300 + 90 > cursor[1] > 300 and accion != [0, 0]:
                    ventana.blit(go1_img, (590, 300))
                    # si se hace click izquierdo en el boton go.....
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        # si el bote esta en orilla izquierda
                        if pos_bote == 0:
                            x_nuevo = 10
                            for i in range(6):
                                if personajes[i].pos == 2 or personajes[i].pos == 4:
                                    personajes[i].x_mas = 10
                        # si el bote esta en orilla derecha
                        else:
                            x_nuevo = -10
                            for i in range(6):
                                if personajes[i].pos == 3 or personajes[i].pos == 5:
                                    personajes[i].x_mas = -10
                # si no le damos click solo mostramos el boton
                else:
                    ventana.blit(go_img, (590, 300))

                # detener el movimiento del bote
                if x >= 620 and pos_bote == 0:
                    x_nuevo = 0
                    for i in range(6):
                        personajes[i].x_mas = 0
                    pos_bote = 1
                    num_movida += 1
                    estado[0], estado[1], estado[2] = estado[0] - accion[0], estado[1] - accion[1], 0
                    for i in range(6):
                        if personajes[i].pos == 2:
                            personajes[i].pos = 3
                            personajes[i].izq_der = 'derecha'
                            personajes[i].rect_x += 900
                        if personajes[i].pos == 4:
                            personajes[i].pos = 5
                            personajes[i].izq_der = 'derecha'
                            personajes[i].rect_x += 900

                if x <= 128 and pos_bote == 1:
                    x_nuevo = 0
                    for i in range(6):
                        personajes[i].x_mas = 0
                    pos_bote = 0
                    num_movida += 1
                    estado[0], estado[1], estado[2] = estado[0] + accion[0], estado[1] + accion[1], 1
                    for i in range(6):
                        if personajes[i].pos == 3:
                            personajes[i].pos = 2
                            personajes[i].rect_x -= 900
                            personajes[i].izq_der = 'izquierda'
                        if personajes[i].pos == 5:
                            personajes[i].pos = 4
                            personajes[i].izq_der = 'izquierda'
                            personajes[i].rect_x -= 900

                # verificar si bote esta lleno
                if accion != [1, 1] and accion != [0, 2] and accion != [2, 0]:
                    for i in range(6):
                        # click para bajar personaje del bote
                        if personajes[i].rect_x + personajes[i].ancho > cursor[0] > personajes[i].rect_x \
                                and personajes[i].rect_y + personajes[i].altura > cursor[1] > personajes[i].rect_y:
                            if personajes[i].pos == 0 and personajes[i].izq_der == 'izquierda' \
                                    and pos_bote == 0:
                                personajes[i].mover()
                                if pygame.mouse.get_pressed() == (1, 0, 0):
                                    if personajes[i].personaje == 'P':
                                        a += 1
                                    elif personajes[i].personaje == 'V':
                                        b += 1
                                    if accion == [0, 1] or accion == [1, 0]:
                                        for k in range(6):
                                            if personajes[k].pos == 2:
                                                izquierda = True
                                            if personajes[k].pos == 4:
                                                derecha = True
                                        if izquierda:
                                            personajes[i].x, personajes[i].y = x + 180, y - 50
                                            personajes[i].pos = 4
                                        elif derecha:
                                            personajes[i].x, personajes[i].y = x + 20, y - 50
                                            personajes[i].pos = 2
                                    else:
                                        personajes[i].x, personajes[i].y = x + 20, y - 50
                                        personajes[i].pos = 2

                            elif personajes[i].pos == 1 and personajes[i].izq_der == 'derecha' and pos_bote == 1:
                                personajes[i].mover()
                                if pygame.mouse.get_pressed() == (1, 0, 0):
                                    if personajes[i].personaje == 'P':
                                        a += 1
                                    elif personajes[i].personaje == 'V':
                                        b += 1
                                    if accion == [0, 1] or accion == [1, 0]:
                                        for k in range(6):
                                            if personajes[k].pos == 3:
                                                izquierda = True
                                            if personajes[k].pos == 5:
                                                derecha = True
                                        if izquierda:
                                            personajes[i].x, personajes[i].y = x + 180, y - 50
                                            personajes[i].pos = 5
                                        elif derecha:
                                            personajes[i].x, personajes[i].y = x + 20, y - 50
                                            personajes[i].pos = 3
                                    else:
                                        personajes[i].x, personajes[i].y = x + 20, y - 50
                                        personajes[i].pos = 3
                                    print(i, personajes[i].x, personajes[i].y)

                # verificar si hay uno o dos personajes en el bote
                if accion != [0, 0]:
                    for j in range(4):
                        if en_bote[j].x + en_bote[j].ancho > cursor[0] > en_bote[j].x and \
                                en_bote[j].y + en_bote[j].altura > cursor[1] > en_bote[j].y:
                            k = 7
                            for i in range(6):
                                if personajes[i].pos == en_bote[j].pos:
                                    k = i
                            if k != 7:
                                en_bote[j].mover(x, y, personajes[k].personaje)
                                if pygame.mouse.get_pressed() == (1, 0, 0):
                                    if personajes[k].personaje == 'P':
                                        a -= 1
                                    elif personajes[k].personaje == 'V':
                                        b -= 1
                                    if personajes[k].izq_der == 'izquierda':
                                        personajes[k].x, personajes[k].y = personajes[k].rect_x - 12, personajes[
                                            k].rect_y
                                        personajes[k].pos = 0
                                    elif personajes[k].izq_der == 'derecha':
                                        personajes[k].x, personajes[k].y = personajes[k].rect_x - 12, personajes[
                                            k].rect_y
                                        personajes[k].pos = 1
                                    if en_bote[j].pos == 2 or en_bote[j].pos == 3:
                                        izquierda = False
                                    elif en_bote[j].pos == 4 or en_bote[j].pos == 5:
                                        derecha = False

                # actualizar la posición del barco para el movimiento
                x = x + x_nuevo

                # actualizar la posicion de los personajes para el movimiento
                for i in range(6):
                    personajes[i].x += personajes[i].x_mas
                accion = [a, b]

            # acciones para fin del juego
            elif fin_juego and not fin_jugador:
                pygame.mixer.music.stop()
                snd_fin.play(0)
                fin_jugador = True

            # acciones para victoria
            elif victoria and not victoria_jugador:
                pygame.mixer.music.stop()
                snd_victoria.play(0)
                victoria_jugador = True

            pygame.display.update()
            clock.tick(25)
            # ejecutamos las acciones del agente
            if con_agente:
                for respuesta in agente.acciones:
                    self.habla.say(respuesta)
                    print(respuesta)
                self.habla.runAndWait()
                con_agente = False

        pygame.quit()
        quit()
