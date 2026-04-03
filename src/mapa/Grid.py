import pygame

class Grid:
    def __init__(self, colunas=50, linhas=50, tile_size=100):
        self.colunas = colunas
        self.linhas = linhas
        self.tile_size = tile_size
        self.celula_selecionada = None 

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

        if self.celula_selecionada:
            self.draw_selection(surface, cam_x, cam_y)

    def draw_selection(self, surface, cam_x, cam_y):
        x, y = self.celula_selecionada
        rect_x = (x * self.tile_size) - cam_x
        rect_y = (y * self.tile_size) - cam_y
        pygame.draw.rect(surface, (255, 255, 0), 
                        (rect_x, rect_y, self.tile_size, self.tile_size), 3)

    def tela_para_grid(self, pos_mouse, cam_x, cam_y):
        x, y = pos_mouse
        grid_x = round((x + cam_x) / self.tile_size)
        grid_y = round((y + cam_y) / self.tile_size)
        
        if 0 <= grid_x < self.colunas and 0 <= grid_y < self.linhas:
            return (grid_x, grid_y)
        return None

    def selecionar_celula(self, pos_mouse, cam_x, cam_y):
        pos_grid = self.tela_para_grid(pos_mouse, cam_x, cam_y)
        if pos_grid:
            self.celula_selecionada = pos_grid
            return True
        return False