class Bote:

    # constructor
    def __init__(self, x, y, pos, imagen1, imagen2, superficie):
        self.x = x
        self.y = y
        self.pos = pos
        self.imagen1 = imagen1
        self.imagen2 = imagen2
        self.superficie = superficie
        self.ancho = 40
        self.altura = 100

    def mover(self, a, b, c):
        if self.pos == 2 or self.pos == 3:
            if c == 'M':
                self.superficie.blit(self.imagen1, (a + 20, b - 50))
            elif c == 'C':
                self.superficie.blit(self.imagen2, (a + 20, b - 50))
        elif self.pos == 4 or self.pos == 5:
            if c == 'M':
                self.superficie.blit(self.imagen1, (a + 180, b - 50))
            elif c == 'C':
                self.superficie.blit(self.imagen2, (a + 180, b - 50))
