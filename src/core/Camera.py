import pygame

class Camera:
    def __init__(self, colunas, linhas, tile_size, velocidade=30):
        self.x = 0
        self.y = 0
        self.zoom_min = 0.5
        self.zoom_max = 1

        self.colunas = colunas
        self.linhas = linhas

        self.tile_base = tile_size
        self.zoom = 1.0
        self.zoom_alvo = 1.0
        self.zoom_velocidade = 0.05 # velocidade do zoom 

        self.tile_size = int(self.tile_base * self.zoom)

        self.velocidade_base = velocidade

        self.mundo_w = colunas * self.tile_size
        self.mundo_h = linhas * self.tile_size

        # Mouse drag
        self.clicando = False
        self.ultima_pos_mouse = (0, 0)

    # parte do zoom
    @property
    def zoom_animando(self):
        return abs(self.zoom - self.zoom_alvo) > 0.001

    def zoom_in(self, largura_tela, altura_tela):
        self._ajustar_zoom(0.1, largura_tela, altura_tela)

    def zoom_out(self, largura_tela, altura_tela):
        self._ajustar_zoom(-0.1, largura_tela, altura_tela)

    def _ajustar_zoom(self, delta, largura_tela, altura_tela):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # posição no mundo antes do zoom
        mundo_x_antes = mouse_x + self.x
        mundo_y_antes = mouse_y + self.y

        # novo zoom alvo
        self.zoom_alvo = max(self.zoom_min, min(self.zoom_max, self.zoom_alvo + delta))

        novo_tile = self.tile_base * self.zoom_alvo
        tile_atual = self.tile_base * self.zoom

        if tile_atual == 0:
            return

        fator = novo_tile / tile_atual

        # zoon focando no mouse (instavel)
        # self.x = mundo_x_antes * fator - mouse_x
        # self.y = mundo_y_antes * fator - mouse_y

    def atualizar_zoom(self, largura_tela, altura_tela):
        if not self.zoom_animando:
            return False

        self.zoom += (self.zoom_alvo - self.zoom) * self.zoom_velocidade

        self.tile_size = int(self.tile_base * self.zoom)

        self.mundo_w = self.colunas * self.tile_size
        self.mundo_h = self.linhas * self.tile_size

        self._aplicar_travas(largura_tela, altura_tela)
        return True

    #movimento da camera
    def _aplicar_travas(self, largura_tela, altura_tela):
        max_x = max(0, self.mundo_w - largura_tela)
        max_y = max(0, self.mundo_h - altura_tela)

        self.x = max(0, min(self.x, max_x))
        self.y = max(0, min(self.y, max_y))

    def mover_por_teclado(self, largura_tela, altura_tela):
        keys = pygame.key.get_pressed()

        velocidade = self.velocidade_base * self.zoom

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= velocidade
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += velocidade
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= velocidade
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += velocidade

        self._aplicar_travas(largura_tela, altura_tela)

    def mover_por_mouse(self, largura_tela, altura_tela):
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        if mouse_buttons[2]:  
            if not self.clicando:
                self.clicando = True
            else:
                dx = mouse_pos[0] - self.ultima_pos_mouse[0]
                dy = mouse_pos[1] - self.ultima_pos_mouse[1]

                self.x -= dx
                self.y -= dy
        else:
            self.clicando = False

        self.ultima_pos_mouse = mouse_pos
        self._aplicar_travas(largura_tela, altura_tela)

    def coordenadas_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return (mouse_x + self.x, mouse_y + self.y)