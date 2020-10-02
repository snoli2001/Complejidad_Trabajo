
from Entites.Player import Player
import pygame

from functions import get_position_from_player_number


class DPlayer(Player):
    def __init__(self, n_player, board, color):
        Player.__init__(self, n_player, board)
        self.n_player = n_player
        self.c = color

    def draw(self, board, surface):
        algorithms = {
            1: 'dijkstra',
            2: 'a_start',
            3: 'bellman',
            4: 'shortest'
        }
        f = pygame.font.Font(None, 20)
        text = f.render(algorithms[self.n_player], True, (255, 255, 255), self.c)
        square_w, square_h = board.square_dimension()
        x, y = get_position_from_player_number(self, board)
        x, y = board.get_position_on_board(x, y, square_w, square_h)
        pygame.draw.ellipse(surface, self.c, (x, y, square_w, square_h))
        surface.blit(text, (x + square_w // 2 - f.size(algorithms[self.n_player])[0] // 2, y + square_h // 2 -\
                            f.size(algorithms[self.n_player])[1] // 2))
