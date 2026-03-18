import pygame
from src.mapa.Mapa import Mapa
from src.mapa.Grid import Grid
from src.core.Camera import Camera

class Engine:
    def __init__(self, tela):
        self.screen = tela
        self.clock = pygame.time.Clock()
        self.running = True

        # Definições do mapa 25x25 com tiles de 100 pixels
        cols, lins, tile = 25, 25, 100
        
        self.mapa = Mapa(id_mapa = 4, tile_size=tile)
        self.grid = Grid(colunas=cols, linhas=lins, tile_size=tile)
        self.camera = Camera(colunas=cols, linhas=lins, tile_size=tile, velocidade=12)

    def start(self):
        while self.running:
            largura_janela, altura_janela = self.screen.get_size()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False

            # 1. Atualiza a posição da câmera (com travas)
            self.camera.update(largura_janela, altura_janela)

            # 2. Renderização
            self.screen.fill((20, 20, 20)) # Fundo escuro
            
            # Desenha o chão primeiro
            self.mapa.draw(self.screen, self.camera.x, self.camera.y)
            
            # Desenha o grid por cima
            self.grid.draw_debug(self.screen, self.camera.x, self.camera.y)
            
            pygame.display.flip()
            self.clock.tick(60)