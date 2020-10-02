import time

import pygame
from random import randint

from Entites.DBoard import DBoard
from Entites.DPlayer import DPlayer
from Entites.Board import Board
from Entites.Player import Player

from functions import rotate, get_player_movement_algorithm


data = {
    1: {'Algorithm': None, 'Total': 0.00, 'Counter': 0, 'Average time': 0.00},
    2: {'Algorithm': None, 'Total': 0.00, 'Counter': 0, 'Average time': 0.00},
    3: {'Algorithm': None, 'Total': 0.00, 'Counter': 0, 'Average time': 0.00},
    4: {'Algorithm': None, 'Total': 0.00, 'Counter': 0, 'Average time': 0.00}
}

for item in data:
    data[item]['Algorithm'] = get_player_movement_algorithm(item).__name__


def save_data_to_file():
    with open('results.txt', 'w') as file:
        for element in data:
            if data[element]['Counter'] > 0:
                data[element]['Average time'] = data[element]['Total'] / data[element]['Counter']
                file.write('Algorithm: ' + str(data[element]['Algorithm']) + '\n')
                file.write('Average time: ' + str(data[element]['Average time']) + '\n' + '\n')


class Game:
    def __init__(self, m, n, n_players):
        self.m, self.n = m, n
        self.n_players = n_players
        self.players = []
        self.board = None

    def draw(self, screen):
        self.board.draw(screen)
        for player in self.players:
            player.draw(self.board, screen)

    def move_current_player(self, n_player):
        current = self.players[n_player]
        prev_pos = current.x, current.y

        start = time.time()
        current.update_position()
        end = time.time()
        duration = end - start

        data[n_player + 1]['Total'] += duration
        data[n_player + 1]['Counter'] += 1

        new_pos = current.x, current.y

        board_center = self.board.m // 2, self.board.n // 2

        rotations = 1
        i = (n_player + 1) % self.n_players
        while i != n_player:
            p = self.players[i]
            prev_pos_p = rotate(prev_pos[0], prev_pos[1], -rotations * 90, board_center)
            new_pos_p = rotate(new_pos[0], new_pos[1], -rotations * 90, board_center)
            p.update_view(prev_pos_p, new_pos_p)
            i = (i + 1) % self.n_players
            rotations = rotations + 1

    def start(self, with_interface, screen_size):
        if with_interface:
            self.start_interface(screen_size)
        else:
            self.start_without_interface()

    def start_without_interface(self):
        self.board = Board(self.m, self.n)

        for i in range(self.n_players):
            player_number = i + 1
            if self.n_players == 2:
                if player_number == 2:
                    player_number = 3
            player = Player(player_number, self.board)
            self.players.append(player)

        done = False
        n_player_turn = randint(0, self.n_players - 1)

        while not done:
            self.move_current_player(n_player_turn)
            if self.players[n_player_turn].is_in_winning_position():
                done = True
            n_player_turn = (n_player_turn + 1) % self.n_players

        save_data_to_file()

    def start_interface(self, screen_size):
        screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption('Quoridor')
        self.board = DBoard(self.m, self.n, 10, 10, screen_size[0] - 10, screen_size[1] - 10, 15, (204, 204, 255))

        for i in range(self.n_players):
            player_number = i + 1
            if self.n_players == 2:
                if player_number == 2:
                    player_number = 3
            player = DPlayer(player_number, self.board, (randint(0, 255), randint(0, 255), randint(0, 255)))
            self.players.append(player)

        pygame.init()

        winner = None
        done = False
        n_player_turn = randint(0, self.n_players - 1)

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            screen.fill((255, 255, 255))
            self.draw(screen)
            pygame.display.flip()
            pygame.time.delay(200)

            self.move_current_player(n_player_turn)
            if self.players[n_player_turn].is_in_winning_position():
                winner = self.players[n_player_turn]
                done = True
            n_player_turn = (n_player_turn + 1) % self.n_players

        print(winner.n_player)
        save_data_to_file()
        pygame.quit()
