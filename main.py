from AgenteMapu import AgenteMapu
from Rio import Rio

if __name__ == "__main__":
    juego = Rio()
    juan = AgenteMapu()
    juan.set_estado_inicial([3,3,1])
    juan.set_estado_meta([0,0,0])
    juego.insertar(juan)
    juego.run()
