class Personaje:

    def __init__(self, x, y, x_mas, pos, personaje, izq_der, imagen1, imagen2, superficie):
        self.izq_der = izq_der
        self.x = x
        self.y = y
        self.x_mas = x_mas
        self.pos = pos
        self.personaje = personaje
        self.rect_x = x + 12
        self.rect_y = y
        self.imagen1 = imagen1
        self.image2 = imagen2
        self.superficie = superficie
        self. ancho = 40
        self.altura = 100

    def mostrar(self):
        self.superficie.blit(self.imagen1, (self.x, self.y))

    def mover(self):
        self.superficie.blit(self.image2, (self.x, self.y))
