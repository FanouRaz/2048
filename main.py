

import numpy as np
import random
import pygame
from pygame.locals import *

from Couleurs import COULEURS_CASES

#Taille de la grille
N = 4


class P2048:
    
    def __init__(self):
        self.grid = np.zeros((N, N), dtype=int)

        self.width = 400
        self.height = self.width
        self.SPACING = 10

        pygame.init()
        icon = pygame.image.load('2048.png')
        pygame.display.set_caption("Py2048")
        pygame.display.set_icon(icon)
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Sans-serif',30)

        self.screen = pygame.display.set_mode((self.width, self.height))

    def __str__(self):
        return str(self.grid)

    def nouvelleCase(self, k=1):
        pos = list(zip(*np.where(self.grid == 0)))
        for randPos in random.sample(pos, k=k):
            if random.random() < 0.1:
                self.grid[randPos] = 4
            else:
                self.grid[randPos] = 2

    @staticmethod
    def _get_nums(this):
        this_n = this[this != 0]
        this_n_sum = []
        skip = False
        for j in range(len(this_n)):
            if skip:
                skip = False
                continue
            if j != len(this_n) - 1 and this_n[j] == this_n[j + 1]:
                new_n = this_n[j] * 2
                skip = True
            else:
                new_n = this_n[j]

            this_n_sum.append(new_n)
        return np.array(this_n_sum)

    def deplacement(self, move):
        for i in range(N):
            if move in 'lr':
                this = self.grid[i, :]
            else:
                this = self.grid[:, i]

            flipped = False
            if move in 'rd':
                flipped = True
                this = this[::-1]

            this_n = self._get_nums(this)

            new_this = np.zeros_like(this)
            new_this[:len(this_n)] = this_n

            if flipped:
                new_this = new_this[::-1]

            if move in 'lr':
                self.grid[i, :] = new_this
            else:
                self.grid[:, i] = new_this

    def grilleJeu(self):
        self.screen.fill(COULEURS_CASES['back'])

        for i in range(N):
            for j in range(N):
                n = self.grid[i][j]

                rectX = j * self.width // N + self.SPACING
                rectY = i * self.height // N + self.SPACING
                rectWidth = self.width // N - 2 * self.SPACING
                rectHeight = self.height // N - 2 * self.SPACING

                pygame.draw.rect(self.screen,
                                 COULEURS_CASES[n],
                                 pygame.Rect(rectX, rectY, rectWidth, rectHeight))
                if n == 0:
                    continue
                text_surface = self.myfont.render(f'{n}', True, ("#FFFFFF"))
                text_rect = text_surface.get_rect(center=(rectX + rectWidth / 2,
                                                          rectY + rectHeight / 2))
                self.screen.blit(text_surface, text_rect)

    @staticmethod
    def wait_for_key():
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 'q'
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        return 'u'
                    elif event.key == K_RIGHT:
                        return 'r'
                    elif event.key == K_LEFT:
                        return 'l'
                    elif event.key == K_DOWN:
                        return 'd'
                    elif event.key == K_q or event.key == K_ESCAPE:
                        return 'q'

    def gameOver(self):
        grid_bu = self.grid.copy()
        for move in 'lrud':
            self.deplacement(move)
            if not all((self.grid == grid_bu).flatten()):
                self.grid = grid_bu
                return False
        return True

    def play(self):
        self.nouvelleCase(k=2)

        while True:
            self.grilleJeu()
            pygame.display.flip()
            cmd = self.wait_for_key()
            if cmd == 'q':
                break

            old_grid = self.grid.copy()
            self.deplacement(cmd)
            if self.gameOver():
                print('Fin de la partie!')
                break

            if not all((self.grid == old_grid).flatten()):
                self.nouvelleCase()


if __name__ == '__main__':
    jeu = P2048()
    jeu.play()