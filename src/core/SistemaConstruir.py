import pygame
from src.core.Construcao import Construcao
from src.mapa.Mapa import Mapa

class SistemaConstruir:
    def __init__(self, cols, lins, grid, camera, screen, mapa):
        self.cols = cols
        self.lins = lins
        self.grid = grid
        self.camera = camera
        self.screen = screen
        self.mapa = mapa
        
        self.construcoes = []
        self.modo_construcao = False
        self.tipo_construcao_atual = 'residencial'
        self.tipos_disponiveis = ['residencial', 'serraria', 'mina', 'pesca']
        self.indice_tipo_atual = 0

    def handle_keydown(self, event):
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

    def handle_mousebuttondown(self, event):
        mouse_pos = pygame.mouse.get_pos()
        pos_grid = self.grid.tela_para_grid(mouse_pos, self.camera.x, self.camera.y)
        
        if pos_grid:
            if event.button == 1: 
                if self.modo_construcao:
                    if not self.tem_construcao(pos_grid):
                        self.construir(pos_grid)
                    else:
                        self.grid.selecionar_celula(mouse_pos, self.camera.x, self.camera.y)
                else:
                    self.grid.selecionar_celula(mouse_pos, self.camera.x, self.camera.y)
            
            elif event.button == 3:  
                self.remover_construcao(pos_grid)

    def atualizar_tile_size(self, tile_size):
        for construcao in self.construcoes:
            construcao.tile_size = tile_size

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
        x, y = pos_grid

        if 0 <= x < self.cols and 0 <= y < self.lins:

            id_tile = self.mapa.dados_mapa[y][x]

            if not self.tem_construcao(pos_grid) and id_tile != 3:
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
            print("")
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

    def update(self):
        self.desenhar_construcoes()
        if self.modo_construcao:
            self.desenhar_previa_construcao()

