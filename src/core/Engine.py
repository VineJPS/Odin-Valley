import pygame
from src.mapa.Mapa import Mapa
from src.mapa.Grid import Grid

class Engine:
    def __init__(self, tela):
        self.screen = tela
        self.clock = pygame.time.Clock()
        self.running = True

        #por hora estatico em apenas 1
        self.mapa_selecionado = 1

        # Componentes do Jogo
        largura, altura = self.screen.get_size()
        self.mapa = Mapa(largura, altura,  self.mapa_selecionado )
        self.grid = Grid(largura, altura)

    def start(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: 
                        self.running = False

            self.mapa.draw(self.screen)
            self.grid.draw_debug(self.screen)
            
            pygame.display.flip()
            self.clock.tick(60)