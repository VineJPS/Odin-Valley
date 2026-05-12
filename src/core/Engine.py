import pygame
from src.mapa.Mapa import Mapa
from src.mapa.Grid import Grid
from src.core.Camera import Camera
from src.ui.Hud import Hud, GerenciamentoHud, recursoHud
from src.dialogos.Dialogo import DialogueSystem
from src.construcao.SistemaConstruir import SistemaConstruir
from src.audio.SoundTrack import GerenciadorMusica
from src.audio.Efeitos import GerenciadorEfeitos
from src.ui.PauseMenu import PauseMenu
from src.core.Ciclos import Ciclos
from src.core.SaveManager import SaveManager


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
        self.estatisticas = GerenciamentoHud(largura - 215, altura + 20, 45, "estatisticas.png", "2", 1.5)
        self.lixo = GerenciamentoHud(largura + 215, altura + 20, 45, "lixo.png", "3", 0.9)

        # Diálogo
        self.dialogo = DialogueSystem(self.screen, largura, altura)
        self.intro_exibida = False
        self.iniciar_intro()

        # Construção
        self.sistema_construir = SistemaConstruir(
            self.cols, self.lins, self.grid, self.camera, self.screen, self.mapa
        )

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

    def iniciar_intro(self):
        if not self.intro_exibida:
            self.dialogo.load_dialogue('falas.json', 'cena_inicial')
            self.intro_exibida = True

    def handle_events(self):
        largura, altura = self.screen.get_size()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            # diálogo
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.dialogo.active:
                    self.dialogo.next_message()

            # bloqueia resto do jogo enquanto diálogo estiver ativo
            if self.dialogo.active:
                continue

            # pause
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.pausado = not self.pausado

            if self.pausado:

                if event.type == pygame.KEYDOWN:
                    self.pause_menu.navegar(event)

                    if event.key == pygame.K_RETURN:
                        opcao = self.pause_menu.selecionar()

                        if opcao == "Continuar":
                            self.pausado = False

                        elif opcao == "Salvar":
                            SaveManager.salvar(self)
                            self.pausado = False

                        elif opcao == "Carregar":
                            SaveManager.carregar(self)
                            self.pausado = False

                        elif opcao == "Voltar ao menu":
                            self.running = False
                            self.musica.soundtrack("menu")

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        opcao = self.pause_menu.clicar(pygame.mouse.get_pos())

                        if opcao == "Continuar":
                            self.pausado = False

                        elif opcao == "Salvar":
                            SaveManager.salvar(self)
                            self.pausado = False

                        elif opcao == "Carregar":
                            SaveManager.carregar(self)
                            self.pausado = False

                        elif opcao == "Voltar ao menu":
                            self.running = False
                            self.musica.soundtrack("menu")

                continue

            # teclas normais
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_F5:
                    SaveManager.salvar(self)

                if event.key == pygame.K_F9:
                    SaveManager.carregar(self)

                if event.key == pygame.K_g:
                    self.mostrar_grid = not self.mostrar_grid

                if event.key == pygame.K_h:
                    self.hud.toggle_controles()

                self.sistema_construir.handle_keydown(event)

            # mouse
            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    if self.martelo.gerenciamento_click(mouse_pos):
                        self.sistema_construir.modo_construcao = (
                            not self.sistema_construir.modo_construcao
                        )
                        continue

                self.sistema_construir.handle_mousebuttondown(event)

            # zoom
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    self.camera.zoom_in(largura, altura)
                else:
                    self.camera.zoom_out(largura, altura)

    def update(self):
        largura, altura = self.screen.get_size()
        dt = self.clock.get_time()

        # pausa lógica também durante diálogo
        if not self.pausado and not self.dialogo.active:

            self.ciclos.update(dt, self.pausado)
            self.recursos_gerenciador.update(dt)

            self.recursos.atualizar_recursos(
                self.recursos_gerenciador.get_recursos()
            )

            self.recursos.elementos[0]['valor'] = int(self.recursos.elementos[0]['valor'])
            self.recursos.elementos[1]['valor'] = int(self.recursos.elementos[1]['valor'])
            self.recursos.elementos[2]['valor'] = int(self.recursos.elementos[2]['valor'])
            self.recursos.elementos[3]['valor'] = int(self.recursos.elementos[3]['valor'])

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

    def draw(self):
        self.screen.fill(self.ciclos.cor_ceu)

        self.mapa.draw_with_night_effect(
            self.screen,
            self.camera.x,
            self.camera.y,
            self.ciclos.is_noite(),
            self.ciclos.get_alpha_sombra()
        )

        self.sistema_construir.desenhar_construcoes()

        if not self.pausado and self.sistema_construir.modo_construcao:
            self.sistema_construir.desenhar_previa_construcao()

        if self.mostrar_grid and not self.pausado:
            self.grid.draw_debug(self.screen, self.camera.x, self.camera.y)

        if not self.pausado and not self.dialogo.active:
            self.hud.desenhar(self.screen)
            self.recursos.exibir_recursos()
            self.hud.desenhar_tempo(self.screen, self.ciclos)
            self.martelo.desenhar_circulo(self.screen)

        # diálogo
        if self.dialogo.active:
            self.dialogo.draw()

        # pause
        if self.pausado:
            self.pause_menu.desenhar()

        pygame.display.flip()

    def start(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
            self.musica.atualizar()