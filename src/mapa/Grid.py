import pygame

class Grid:
    def __init__(self, tela_w, tela_h, colunas=20, linhas=15):
        self.colunas = colunas
        self.linhas = linhas
        
        # O tamanho do tile baseado na largura da tela
        self.tile_size = tela_w // colunas
        
        # Inicializa a matriz preenchida com zeros
        self.data = [[0 for _ in range(self.colunas)] for _ in range(self.linhas)]

    def draw_debug(self, surface):
        """Desenha as linhas do grid para orientação"""
        cor = (255, 255, 255, 30)
        
        largura_total = self.colunas * self.tile_size
        altura_total = self.linhas * self.tile_size

        # Desenha linhas verticais
        for c in range(self.colunas + 1):
            x = c * self.tile_size
            pygame.draw.line(surface, cor, (x, 0), (x, altura_total))
            
        # Desenha linhas horizontais
        for l in range(self.linhas + 1):
            y = l * self.tile_size
            pygame.draw.line(surface, cor, (0, y), (largura_total, y))