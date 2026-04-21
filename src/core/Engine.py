import pygame
from src.mapa.Mapa import Mapa
from src.mapa.Grid import Grid
from src.core.Camera import Camera
from src.ui.Hud import Hud, GerenciamentoHud, recursoHud
from src.core.Construcao import Construcao
from src.core.SistemaConstruir import SistemaConstruir
from src.audio.SoundTrack import GerenciadorMusica
from src.audio.Efeitos import GerenciadorEfeitos
from src.ui.PauseMenu import PauseMenu

class Engine:
    def __init__(self, tela):
        self.screen = tela
        self.clock = pygame.time.Clock()
        self.running = True
        self.mostrar_grid = False
        self.pausado = False

        # Mundo
        self.mapa = Mapa(id_mapa=1, tile_size=100)
        self.cols = len(self.mapa.dados_mapa[0])
        self.lins = len(self.mapa.dados_mapa)

        self.grid = Grid(self.cols, self.lins, 100)
        self.camera = Camera(self.cols, self.lins, 100, velocidade=12)

        # HUD
        largura, altura = self.screen.get_size()
        self.hud = Hud(largura, altura)
        self.recursos = recursoHud(self.screen)

        self.martelo = GerenciamentoHud(largura, altura, 60, "Martelo.png", "B", 1.5)
        self.estatisticas = GerenciamentoHud(largura-215, altura+20, 45, "estatisticas.png", "2", 1.5)
        self.lixo = GerenciamentoHud(largura+215, altura+20, 45, "lixo.png", "3", 0.9)

        # Construção
        self.sistema_construir = SistemaConstruir(
            self.cols, self.lins, self.grid, self.camera, self.screen, self.mapa
        )
        self.construcoes_persistentes = []

        # Pause
        self.pause_menu = PauseMenu(self.screen)

        # Áudio
        self.efeitos = GerenciadorEfeitos()
        self.musica = GerenciadorMusica()
        self.musica.criar_playlist_aleatoria()

    def handle_events(self):
        largura, altura = self.screen.get_size()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.pausado = not self.pausado

            if self.pausado:
                if event.type == pygame.KEYDOWN:
                    self.pause_menu.navegar(event)

                    if event.key == pygame.K_RETURN:
                        opcao = self.pause_menu.selecionar()

                        if opcao == "Continuar":
                            self.pausado = False

                        elif opcao == "Voltar ao menu":
                            self.running = False
                            self.musica.soundtrack("menu")

            # clicar no menu de pause
            if self.pausado and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    opcao = self.pause_menu.clicar(pygame.mouse.get_pos())

                    if opcao == "Continuar":
                        self.pausado = False

                    elif opcao == "Voltar ao menu":
                        self.running = False
                        self.musica.parar()
                        self.musica.soundtrack("menu")

                continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    self.mostrar_grid = not self.mostrar_grid

                if event.key == pygame.K_h:
                    self.hud.toggle_controles()

                self.sistema_construir.handle_keydown(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.sistema_construir.handle_mousebuttondown(event)

            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    self.camera.zoom_in(largura, altura)
                else:
                    self.camera.zoom_out(largura, altura)


    # parte da lógica 
    def update(self):
        largura, altura = self.screen.get_size()

        if self.pausado:
            return  

        self.camera.mover_por_teclado(largura, altura)
        self.camera.mover_por_mouse(largura, altura)
        self.camera.coordenadas_mouse()

        # HUD 
        if self.sistema_construir.modo_construcao:
            self.hud.estado_hud = "construcao"
        else:
            self.hud.estado_hud = "controles"

        # Zoom 
        if self.camera.atualizar_zoom(largura, altura):
            novo_tile = self.camera.tile_size

            self.mapa.tile_size = novo_tile
            self.grid.tile_size = novo_tile
            self.sistema_construir.atualizar_tile_size(novo_tile)


    # renderização
    def draw(self):
        self.screen.fill((20, 20, 20))

        self.mapa.draw(self.screen, self.camera.x, self.camera.y)

        self.sistema_construir.desenhar_construcoes()

        if not self.pausado and self.sistema_construir.modo_construcao:
            self.sistema_construir.desenhar_previa_construcao()

        if self.mostrar_grid and not self.pausado:
            self.grid.draw_debug(self.screen, self.camera.x, self.camera.y)

        if not self.pausado:
            self.hud.desenhar(self.screen)
            self.recursos.exibir_recursos()
            # self.martelo.desenhar_circulo(self.screen)
            # self.estatisticas.desenhar_circulo(self.screen)
            # self.lixo.desenhar_circulo(self.screen)

        # menu de pause
        if self.pausado:
            self.pause_menu.desenhar()

        pygame.display.flip()

    # loop principal
    def start(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
            self.musica.atualizar()