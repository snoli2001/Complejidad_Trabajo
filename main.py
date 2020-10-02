
from Entites.Game import Game

n_players = int(input('Ingrese el numero de jugadores (2 o 4): '))

if n_players != 2 and n_players != 4:
    n_players = 2

m = int(input('Ingrese el numero de filas : '))
n = int(input('Ingrese el numero de columnas: '))

show_interface = input('Desea visualizar la interfaz gráfica del juego? (S, N): ')
screen_size = None

if show_interface[0].lower() == 's':
    show_interface = True
    screen_size = int(input('Ingrese el tamaño de la ventana del juego (solo un número): '))
    screen_size = (screen_size, screen_size)
else:
    show_interface = False

g = Game(m, n, n_players)
g.start(show_interface, screen_size)
