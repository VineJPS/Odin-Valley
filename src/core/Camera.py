import pygame
import math

class Camera:
    def __init__(self, colunas, linhas, tile_size, velocidade=30):
        self.x = 0
        self.y = 0
        self.velocidade = velocidade
        self.colunas = colunas
        self.linhas = linhas
        self.tile_size = float(tile_size)
        self.tile_alvo = float(tile_size)
        self.zoom_velocidade = 0.15
        self.mundo_w = colunas * tile_size
        self.mundo_h = linhas * tile_size
        self.clicando = False
        self.ultima_pos_mouse = (0, 0)

    @property
    def zoom_animando(self):
        return abs(self.tile_size - self.tile_alvo) > 0.50

    def zoom_in(self, largura_tela, altura_tela, passo=10):
        self._definir_alvo(passo, largura_tela, altura_tela)

    def zoom_out(self, largura_tela, altura_tela, passo=10):
        self._definir_alvo(-passo, largura_tela, altura_tela)

    def _definir_alvo(self, delta, largura_tela, altura_tela):
        minimo = max(50, math.ceil(largura_tela / self.colunas), math.ceil(altura_tela / self.linhas))
        self.tile_alvo = max(50.0, min(200.0, self.tile_alvo + delta))

    def atualizar_zoom(self, largura_tela, altura_tela):
        """Deve ser chamado todo frame. Interpola tile_size em direção ao tile_alvo."""
        if not self.zoom_animando:
            return False

        minimo = max(50, math.ceil(largura_tela / self.colunas), math.ceil(altura_tela / self.linhas))
        fator_anterior = self.tile_size
        self.tile_size += (self.tile_alvo - self.tile_size) * self.zoom_velocidade
        self.tile_size = max(40.0, min(200.0, self.tile_size))

        fator = self.tile_size / fator_anterior
        self.mundo_w = self.colunas * self.tile_size
        self.mundo_h = self.linhas * self.tile_size
        self.x = self.x * fator
        self.y = self.y * fator
        self._aplicar_travas(largura_tela, altura_tela)
        return True

    def _aplicar_travas(self, largura_tela, altura_tela):
        """Impede que a câmera saia das bordas do mapa (Clamping)."""
        self.x = max(0, min(self.x, max(0, self.mundo_w - largura_tela)))
        self.y = max(0, min(self.y, max(0, self.mundo_h - altura_tela)))

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
        if mouse_buttons[2]: 
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