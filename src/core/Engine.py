import pygame
from src.mapa.Mapa import Mapa
from src.mapa.Grid import Grid

class Engine:
    def __init__(self, tela):
        self.screen = tela
        self.clock = pygame.time.Clock()
        self.running = True

        self.mapa_selecionado = 1
        # Ajuste: Mapa agora recebe apenas o ID para carregar a matriz interna
        self.mapa = Mapa(self.mapa_selecionado)
        
        largura, altura = self.screen.get_size()
        self.grid = Grid(largura, altura)

    def start(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: 
                        self.running = False

            # Ajuste: Limpa a tela antes de desenhar o novo frame
            self.screen.fill((0, 0, 0))

            # Chamada da função
            self.mapa.draw(self.screen)
            
            #caso queira visualizar o grid na tela
            #self.grid.draw_debug(self.screen)
            pygame.display.flip()
            self.clock.tick(60)