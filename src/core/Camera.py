import pygame

class Camera:
    def __init__(self, colunas, linhas, tile_size, velocidade=10):
        self.x = 0
        self.y = 0
        self.velocidade = velocidade
        
        # Dimensões totais do mundo em pixels
        self.mundo_w = colunas * tile_size
        self.mundo_h = linhas * tile_size

    def update(self, largura_tela, altura_tela):
        keys = pygame.key.get_pressed()
        
        # Movimentação básica
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  self.x -= self.velocidade
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: self.x += self.velocidade
        if keys[pygame.K_w] or keys[pygame.K_UP]:    self.y -= self.velocidade
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  self.y += self.velocidade

        # TRAVAS (Clamping): Impede a câmera de mostrar o que está fora do grid
        self.x = max(0, min(self.x, self.mundo_w - largura_tela))
        self.y = max(0, min(self.y, self.mundo_h - altura_tela))