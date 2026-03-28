import pygame

class Construcao:
    def __init__(self, tipo, posicao_grid, tile_size):
        self.tipo = tipo  
        self.posicao = posicao_grid  
        self.tile_size = tile_size
        
        # cores e nomes temporarios para as construções. enquanto n tiver os sprites
        self.cores = {
            'residencial': (255, 0, 0),        
            'serraria': (200, 150, 100),     
            'mina': (137, 137, 137),          
            'pesca': (100, 150, 200)         
        }
        self.icones = {
            'residencial': 'casa',
            'serraria': 'serraria',
            'mina': 'mina',
            'pesca': 'pesqueiro'
        }
        
    
    def desenhar(self, surface, cam_x, cam_y):
        x = (self.posicao[0] * self.tile_size) - cam_x
        y = (self.posicao[1] * self.tile_size) - cam_y

        cor = self.cores.get(self.tipo, (200, 200, 200))
        pygame.draw.rect(surface, cor, (x, y, self.tile_size, self.tile_size))
        pygame.draw.rect(surface, (0, 0, 0), (x, y, self.tile_size, self.tile_size), 2)

        try:
            fonte = pygame.font.Font(None, int(self.tile_size * 0.6))
            texto = fonte.render(self.icones.get(self.tipo, '?'), True, (255, 255, 255))
            texto_rect = texto.get_rect(center=(x + self.tile_size//2, y + self.tile_size//2))
            surface.blit(texto, texto_rect)
        except:
            pass 