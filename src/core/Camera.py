import pygame

class Camera:
    def __init__(self, colunas, linhas, tile_size, velocidade=10):
        self.x = 0
        self.y = 0
        self.velocidade = velocidade
        
        # Dimensões totais do mundo em pixels
        self.mundo_w = colunas * tile_size
        self.mundo_h = linhas * tile_size
        
        # Auxiliares para o arrasto do mouse
        self.clicando = False
        self.ultima_pos_mouse = (0, 0)

    def _aplicar_travas(self, largura_tela, altura_tela):
        """Impede que a câmera saia das bordas do mapa (Clamping)."""
        self.x = max(0, min(self.x, self.mundo_w - largura_tela))
        self.y = max(0, min(self.y, self.mundo_h - altura_tela))

    def mover_por_teclado(self, largura_tela, altura_tela):
        """Controla a câmera usando WASD ou Setas."""
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  self.x -= self.velocidade
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: self.x += self.velocidade
        if keys[pygame.K_w] or keys[pygame.K_UP]:    self.y -= self.velocidade
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  self.y += self.velocidade

        self._aplicar_travas(largura_tela, altura_tela)

    def mover_por_mouse(self, largura_tela, altura_tela):
        """Controla a câmera clicando e arrastando (Botão Esquerdo)."""
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        
        # Botão [0] é o Esquerdo. Se quiser o Direito, use [2].
        if mouse_buttons[0]: 
            if not self.clicando:
                self.clicando = True
            else:
                # Calcula o deslocamento (delta) do mouse
                dx = mouse_pos[0] - self.ultima_pos_mouse[0]
                dy = mouse_pos[1] - self.ultima_pos_mouse[1]
                
                # Move a câmera (sentido oposto ao mouse para "puxar" o chão)
                self.x -= dx
                self.y -= dy
        else:
            self.clicando = False
            
        self.ultima_pos_mouse = mouse_pos
        self._aplicar_travas(largura_tela, altura_tela)

    def coordenadas_mouse(self):
        """Converte a posição do mouse na tela para a posição no mapa real."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return (mouse_x + self.x, mouse_y + self.y)