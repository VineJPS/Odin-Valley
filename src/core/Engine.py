import pygame
from src.mapa.Mapa import Mapa
from src.mapa.Grid import Grid
from src.core.Camera import Camera
from src.ui.Hud import Hud,GerenciamentoHud,recursoHud
from src.core.Construcao import Construcao
from src.core.SistemaConstruir import SistemaConstruir
from src.audio.SoundTrack import GerenciadorMusica
from src.audio.Efeitos import GerenciadorEfeitos

class Engine:
    def __init__(self, tela):
        self.screen = tela
        self.clock = pygame.time.Clock()
        self.running = True
        self.mostrar_grid = False

        self.mapa = Mapa(id_mapa=1, tile_size=100)
        self.cols = len(self.mapa.dados_mapa[0])
        self.lins = len(self.mapa.dados_mapa)
        self.grid   = Grid(colunas=self.cols, linhas=self.lins, tile_size=100)
        self.camera = Camera(colunas=self.cols, linhas=self.lins, tile_size=100, velocidade=12)

        # necessario para renderizar o hud
        largura_janela, altura_janela = self.screen.get_size()
        self.hud = Hud(largura_janela, altura_janela)
        self.recursos = recursoHud(self.screen)
        self.martelo = GerenciamentoHud(largura_janela, altura_janela, 60, "Martelo.png", "1", 1.5)
        self.estatisticas = GerenciamentoHud(largura_janela-215, altura_janela+20, 45, "estatisticas.png", "2", 1.5)
        self.lixo = GerenciamentoHud(largura_janela+215, altura_janela+20, 45, "lixo.png", "3", 0.9)
        
        self.sistema_construir = SistemaConstruir(self.cols, self.lins, self.grid, self.camera, self.screen, self.mapa)

        # Iniciando os gereciadores de som
        self.efeitos = GerenciadorEfeitos()
        self.musica = GerenciadorMusica()

    def start(self):
        while self.running:
            largura_janela, altura_janela = self.screen.get_size()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.musica.soundtrack("menu")

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        self.mostrar_grid = not self.mostrar_grid
                    if event.key == pygame.K_h:
                        self.hud.toggle_controles()
                    
                    self.sistema_construir.handle_keydown(event)
                    
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: 
                        mouse_pos = pygame.mouse.get_pos()
                        pos_grid = self.grid.tela_para_grid(mouse_pos, self.camera.x, self.camera.y)
                        
                        self.sistema_construir.handle_mousebuttondown(event)
        
                    elif event.button == 3:
                        self.sistema_construir.handle_mousebuttondown(event)

                if event.type == pygame.MOUSEWHEEL:
                    if event.y > 0:
                        self.camera.zoom_in(largura_janela, altura_janela)
                    else:
                        self.camera.zoom_out(largura_janela, altura_janela)

            if self.camera.atualizar_zoom(largura_janela, altura_janela):
                self.mapa = Mapa(id_mapa=1, tile_size=self.camera.tile_size)
                self.cols = len(self.mapa.dados_mapa[0])
                self.lins = len(self.mapa.dados_mapa)
                self.grid = Grid(colunas=self.cols, linhas=self.lins, tile_size=self.camera.tile_size)
                self.camera = Camera(colunas=self.cols, linhas=self.lins, tile_size=self.camera.tile_size, velocidade=12)
                self.sistema_construir = SistemaConstruir(self.cols, self.lins, self.grid, self.camera, self.screen, self.mapa)

            self.camera.mover_por_teclado(largura_janela, altura_janela)
            self.camera.mover_por_mouse(largura_janela, altura_janela)
            self.camera.coordenadas_mouse()
            
            # Renderização
            self.screen.fill((20, 20, 20))
            self.mapa.draw(self.screen, self.camera.x, self.camera.y)
            self.sistema_construir.update()
            if self.mostrar_grid:
                self.grid.draw_debug(self.screen, self.camera.x, self.camera.y)
            self.hud.desenhar(self.screen)
            self.recursos.exibir_recursos()
            self.martelo.desenhar_circulo(self.screen)
            self.estatisticas.desenhar_circulo(self.screen)
            self.lixo.desenhar_circulo(self.screen)

            pygame.display.flip()
            self.clock.tick(60)