import pygame

class Grid:
    def __init__(self, colunas=25, linhas=25, tile_size=100):
        self.colunas = colunas
        self.linhas = linhas
        self.tile_size = tile_size

    def draw_debug(self, surface, cam_x, cam_y):
        cor_linha = (255, 255, 255, 40) # Branco suave
        
        largura_total = self.colunas * self.tile_size
        altura_total = self.linhas * self.tile_size

        # Desenha as linhas verticais
        for c in range(self.colunas + 1):
            x = (c * self.tile_size) - cam_x
            pygame.draw.line(surface, cor_linha, (x, -cam_y), (x, altura_total - cam_y))
            
        # Desenha as linhas horizontais
        for l in range(self.linhas + 1):
            y = (l * self.tile_size) - cam_y
            pygame.draw.line(surface, cor_linha, (-cam_x, y), (largura_total - cam_x, y))