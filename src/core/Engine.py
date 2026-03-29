import pygame
from src.mapa.Mapa import Mapa
from src.mapa.Grid import Grid
from src.core.Camera import Camera
from src.ui.Hud import Hud
from src.core.Construcao import Construcao

class Engine:
    def __init__(self, tela):
        self.screen = tela
        self.clock = pygame.time.Clock()
        self.running = True
        self.mostrar_grid = False

        # Definições do mapa 25x25 com tiles de 100 pixels
        self.cols, self.lins, tile = 25, 25, 100
        self.mapa   = Mapa(id_mapa=4, tile_size=tile)
        self.grid   = Grid(colunas=self.cols, linhas=self.lins, tile_size=tile)
        self.camera = Camera(colunas=self.cols, linhas=self.lins, tile_size=tile, velocidade=12)

        # necessario para renderizar o hud
        largura_janela, altura_janela = self.screen.get_size()
        self.hud = Hud(largura_janela, altura_janela)
        
        # parte das contruções
        self.construcoes = []  
        self.modo_construcao = False
        self.tipo_construcao_atual = 'residencial'
        self.tipos_disponiveis = ['residencial', 'serraria', 'mina', 'pesca']
        self.indice_tipo_atual = 0

    def start(self):
        while self.running:
            largura_janela, altura_janela = self.screen.get_size()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        self.mostrar_grid = not self.mostrar_grid
                    if event.key == pygame.K_h:
                        self.hud.toggle_controles()
                    
                    # alternar  entre os modos
                    if event.key == pygame.K_b:
                        self.modo_construcao = not self.modo_construcao
                        print(f"Modo {'CONSTRUÇÃO' if self.modo_construcao else 'SELEÇÃO'}")
                    
                    if event.key == pygame.K_1:
                        self.tipo_construcao_atual = 'residencial'
                        self.indice_tipo_atual = self.tipos_disponiveis.index('residencial')
                    if event.key == pygame.K_2:
                        self.tipo_construcao_atual = 'serraria'
                        self.indice_tipo_atual = self.tipos_disponiveis.index('serraria')
                    if event.key == pygame.K_3:
                        self.tipo_construcao_atual = 'mina'
                        self.indice_tipo_atual = self.tipos_disponiveis.index('mina')
                    if event.key == pygame.K_4:
                        self.tipo_construcao_atual = 'pesca'
                        self.indice_tipo_atual = self.tipos_disponiveis.index('pesca')
                    
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: 
                        mouse_pos = pygame.mouse.get_pos()
                        pos_grid = self.grid.tela_para_grid(mouse_pos, self.camera.x, self.camera.y)
                        
                        if pos_grid:
                            if self.modo_construcao:
                                if not self.tem_construcao(pos_grid):
                                    self.construir(pos_grid)
                                else:
                                    self.grid.selecionar_celula(mouse_pos, self.camera.x, self.camera.y)
                            else:
                                self.grid.selecionar_celula(mouse_pos, self.camera.x, self.camera.y)
                    
                    elif event.button == 3: 
                        mouse_pos = pygame.mouse.get_pos()
                        pos_grid = self.grid.tela_para_grid(mouse_pos, self.camera.x, self.camera.y)
                        if pos_grid:
                            self.remover_construcao(pos_grid)

                if event.type == pygame.MOUSEWHEEL:
                    if event.y > 0:
                        self.camera.zoom_in(largura_janela, altura_janela)
                    else:
                        self.camera.zoom_out(largura_janela, altura_janela)

            if self.camera.atualizar_zoom(largura_janela, altura_janela):
                self.mapa = Mapa(id_mapa=4, tile_size=int(self.camera.tile_size))
                self.grid = Grid(colunas=self.cols, linhas=self.lins, tile_size=int(self.camera.tile_size))
                for construcao in self.construcoes:
                    construcao.tile_size = int(self.camera.tile_size)

            self.camera.mover_por_teclado(largura_janela, altura_janela)
            self.camera.mover_por_mouse(largura_janela, altura_janela)
            self.camera.coordenadas_mouse()
            
            # Renderização
            self.screen.fill((20, 20, 20))
            self.mapa.draw(self.screen, self.camera.x, self.camera.y)
            self.desenhar_construcoes()
            if self.mostrar_grid:
                self.grid.draw_debug(self.screen, self.camera.x, self.camera.y)
            if self.modo_construcao:
                self.desenhar_previa_construcao()
            self.hud.desenhar(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        
    # metodos do menu de contruir
    def tem_construcao(self, pos_grid):
        for construcao in self.construcoes:
            if construcao.posicao == pos_grid:
                return True
        return False
    
    def get_construcao(self, pos_grid):
        for construcao in self.construcoes:
            if construcao.posicao == pos_grid:
                return construcao
        return None
    
    def construir(self, pos_grid):
        if 0 <= pos_grid[0] < self.cols and 0 <= pos_grid[1] < self.lins:
            if not self.tem_construcao(pos_grid):
                nova_construcao = Construcao(
                    self.tipo_construcao_atual,
                    pos_grid,
                    int(self.camera.tile_size)
                )
                self.construcoes.append(nova_construcao)
                return True 
        return False
    
    def remover_construcao(self, pos_grid):
        construcao = self.get_construcao(pos_grid)
        if construcao:
            self.construcoes.remove(construcao)
            print(f"")
            return True
        return False
    
    def desenhar_construcoes(self):
        for construcao in self.construcoes:
            construcao.desenhar(self.screen, self.camera.x, self.camera.y)
    
    def desenhar_previa_construcao(self):
        mouse_pos = pygame.mouse.get_pos()
        pos_grid = self.grid.tela_para_grid(mouse_pos, self.camera.x, self.camera.y)
        
        if pos_grid and not self.tem_construcao(pos_grid):
            x = (pos_grid[0] * self.camera.tile_size) - self.camera.x
            y = (pos_grid[1] * self.camera.tile_size) - self.camera.y
            
            surface = pygame.Surface((self.camera.tile_size, self.camera.tile_size), pygame.SRCALPHA)
            
            # Cores da previa
            cores_previa = {
                'residencial': (255, 0, 0, 128),       
                'serraria': (200, 150, 100, 128),      
                'mina': (137, 137, 137, 128),          
                'pesca': (100, 150, 200, 128)           
            }
            
            cor = cores_previa.get(self.tipo_construcao_atual, (200, 200, 200, 128))
            surface.fill(cor)
            pygame.draw.rect(surface, (255, 255, 0), (0, 0, self.camera.tile_size, self.camera.tile_size), 2)
            
            self.screen.blit(surface, (x, y))