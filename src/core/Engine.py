import pygame
from src.mapa.Mapa import Mapa
from src.mapa.Grid import Grid
from src.core.Camera import Camera
from src.ui.Hud import Hud

class Engine:
    def __init__(self, tela):
        self.screen = tela
        self.clock = pygame.time.Clock()
        self.running = True
        self.mostrar_grid = False

        # Definições do mapa 25x25 com tiles de 100 pixels - Sempre que for alterar o tamanho do mapa, mude aqui.
        cols, lins, tile = 25, 25, 100
        
        self.mapa = Mapa(id_mapa = 4, tile_size=tile)
        self.grid = Grid(colunas=cols, linhas=lins, tile_size=tile)
        self.camera = Camera(colunas=cols, linhas=lins, tile_size=tile, velocidade=12)

        #necessario para renderizar o hud
        largura_janela, altura_janela = self.screen.get_size()        
        self.hud = Hud(largura_janela, altura_janela)

    def start(self):
        while self.running:
            largura_janela, altura_janela = self.screen.get_size()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                # Faz o grid aparecer com G
                if event.type == pygame.KEYDOWN:  
                    if event.key == pygame.K_g:   
                        self.mostrar_grid = not self.mostrar_grid  
                    if event.key == pygame.K_h:
                        self.hud.toggle_controles()

            # 1. Atualiza a posição da câmera (com travas)
            self.camera.mover_por_teclado(largura_janela, altura_janela)
            self.camera.mover_por_mouse(largura_janela, altura_janela)
            self.camera.coordenadas_mouse()
            
            # 2. Renderização
            self.screen.fill((20, 20, 20)) # Fundo escuro
            
            # Desenha o chão primeiro
            self.mapa.draw(self.screen, self.camera.x, self.camera.y)
            
            # Desenha o grid por cima
            if self.mostrar_grid:
                self.grid.draw_debug(self.screen, self.camera.x, self.camera.y)
            # desenha o menu dos controles
            self.hud.desenhar(self.screen)

            pygame.display.flip()
            self.clock.tick(60)