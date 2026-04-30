import pygame
from src.mapa.Mapa import Mapa
from src.mapa.Grid import Grid
from src.core.Camera import Camera
from src.ui.Hud import Hud, GerenciamentoHud, recursoHud
from src.dialogos.Dialogo import DialogueSystem
from src.construcao.Construcao import Construcao
from src.construcao.SistemaConstruir import SistemaConstruir
from src.audio.SoundTrack import GerenciadorMusica
from src.audio.Efeitos import GerenciadorEfeitos
from src.ui.PauseMenu import PauseMenu
from src.core.Ciclos import Ciclos

class Engine:
    def __init__(self, tela):
        self.screen = tela
        self.clock = pygame.time.Clock()
        self.running = True
        self.mostrar_grid = False
        self.pausado = False

        # Mundo
        self.mapa = Mapa(id_mapa=3, tile_size=100)
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

        # Dialogos
        self.dialogo = DialogueSystem(self.screen, largura, altura)
        self.dialogo.load_dialogue('falas.json', 'cena_inicial')

        # Construção
        self.sistema_construir = SistemaConstruir(
            self.cols, self.lins, self.grid, self.camera, self.screen, self.mapa
        )
        self.construcoes_persistentes = []

        # Recursos
        from src.construcao.Recursos import GerenciadorRecursos
        self.ciclos = Ciclos()
        self.recursos_gerenciador = GerenciadorRecursos(self.sistema_construir, self.ciclos)

        # Pause
        self.pause_menu = PauseMenu(self.screen)

        # Áudio
        self.efeitos = GerenciadorEfeitos()
        self.musica = GerenciadorMusica()
        self.musica.criar_playlist_aleatoria()

    def handle_events(self):
        largura, altura = self.screen.get_size()

        for event in pygame.event.get():

            def handle_mousebuttondown(self, event):
                if event.type != pygame.MOUSEBUTTONDOWN:
                    return

                mouse_pos = pygame.mouse.get_pos()
                pos_grid = self.grid.tela_para_grid(mouse_pos, self.camera.x, self.camera.y)

                if pos_grid:
                    if event.button == 1:
                            if self.modo_construcao:
                                self.construir(pos_grid)

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.dialogo.active:
                    self.dialogo.next_message()

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
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    if self.martelo.gerenciamento_click(mouse_pos):
                        self.sistema_construir.modo_construcao = not self.sistema_construir.modo_construcao
                        return

                self.sistema_construir.handle_mousebuttondown(event)

            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    self.camera.zoom_in(largura, altura)
                else:
                    self.camera.zoom_out(largura, altura)


    # parte da lógica 
    def update(self):
        largura, altura = self.screen.get_size()
        dt = self.clock.get_time()

        if not self.pausado:
            self.ciclos.update(dt, self.pausado)
            self.recursos_gerenciador.update(dt)
            self.recursos.atualizar_recursos(self.recursos_gerenciador.get_recursos())
            self.recursos.elementos[0]['valor'] = int(self.recursos.elementos[0]['valor'])  # Floor pra int HUD
            self.recursos.elementos[1]['valor'] = int(self.recursos.elementos[1]['valor'])
            self.recursos.elementos[2]['valor'] = int(self.recursos.elementos[2]['valor'])
            self.recursos.elementos[3]['valor'] = int(self.recursos.elementos[3]['valor'])
            self.camera.mover_por_teclado(largura, altura)
            self.camera.mover_por_mouse(largura, altura)
            self.camera.coordenadas_mouse()
        else:
            # Pausa câmera também
            pass

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
        self.screen.fill(self.ciclos.cor_ceu)

        self.mapa.draw_with_night_effect(self.screen, self.camera.x, self.camera.y, self.ciclos.is_noite(), self.ciclos.get_alpha_sombra())

        self.sistema_construir.desenhar_construcoes()

        if not self.pausado and self.sistema_construir.modo_construcao:
            self.sistema_construir.desenhar_previa_construcao()

        if self.mostrar_grid and not self.pausado:
            self.grid.draw_debug(self.screen, self.camera.x, self.camera.y)

        if (not self.pausado) & (not self.dialogo.active):
            self.hud.desenhar(self.screen)
            self.recursos.exibir_recursos()
            self.hud.desenhar_tempo(self.screen, self.ciclos)
            self.martelo.desenhar_circulo(self.screen)
            # self.estatisticas.desenhar_circulo(self.screen)
            # self.lixo.desenhar_circulo(self.screen)

        # Quando o dialogo fica ativo
        if self.dialogo.active:
            self.dialogo.draw()

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