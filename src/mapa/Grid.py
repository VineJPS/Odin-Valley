import pygame

class Grid:
    def __init__(self, tela_w, tela_h, colunas=20, linhas=15):
        self.e  = colunas
        self.linhas = linhas
        self.tile_size = tela_w // colunas
        self.data = [[0 for _ in range(colunas)] for _ in range(linhas)]

    def draw_debug(self, surface):
        """Desenha as linhas do grid para orientação"""
        cor = (255, 255, 255, 30)
        for c in range(self.colunas + 1):
            x = c * self.tile_size
            pygame.draw.line(surface, cor, (x, 0), (x, surface.get_height()))
        for l in range(self.linhas + 1):
            y = l * self.tile_size
            pygame.draw.line(surface, cor, (0, y), (surface.get_width(), y))