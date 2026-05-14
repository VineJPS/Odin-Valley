import pygame
from .Construcao import Construcao
from src.mapa.Mapa import Mapa
from src.construcao.Recursos import GerenciadorRecursos

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
        self.tipos_disponiveis = ['residencial', 'serraria', 'mina', 'fazenda','pesca']
        self.indice_tipo_atual = 0
        self.imagens_previa = {
            'residencial': pygame.image.load("assets/img/sprites/construcao/Casa.png").convert_alpha(),
            # 'serraria': pygame.image.load("assets/img/sprites/construcao/...").convert_alpha(),
            # 'mina': pygame.image.load("assets/img/sprites/construcao/...").convert_alpha(),
            # 'fazenda': pygame.image.load("assets/img/sprites/construcao/...").convert_alpha(),
            'pesca': pygame.image.load("assets/img/sprites/construcao/pesqueiro.png").convert_alpha(),
        }
        self.cores_previa = {
            'residencial': (255, 0, 0, 120),
            'serraria': (200, 150, 100, 120),
            'mina': (137, 137, 137, 120),
            'fazenda': (150, 100, 100, 120), 
            'pesca': (100, 150, 200, 120),
        }
        self.cache_previa = {}

        self.tamanho_construcoes = {
        'residencial': (2, 2),
        'serraria': (2, 2),
        'mina': (2, 2),
        'fazenda': (2, 2),
        'pesca': (2, 2),
        'base_jogador': (4, 3),
        'base_oponente': (4, 3)
        }

        self.custos = {
            'residencial': {
                'madeira': 15,
                'pedra': 5
            },
            'serraria': {
                'madeira': 30,
                'pedra': 15
            },
            'mina': {
                'madeira': 25,
                'pedra': 15
            },
            'fazenda': {
                'madeira': 25,
                'pedra': 10
            },
            'pesca': {
                'madeira': 15,
                'pedra': 5
            }
        }

    def handle_keydown(self, event):
        if event.key == pygame.K_b:
            self.modo_construcao = not self.modo_construcao
            # print(f"Modo {'CONSTRUÇÃO' if self.modo_construcao else 'SELEÇÃO'}")
        
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
            self.tipo_construcao_atual = 'fazenda'
            self.indice_tipo_atual = self.tipos_disponiveis.index('fazenda')
        if event.key == pygame.K_5:
            self.tipo_construcao_atual = 'pesca'
            self.indice_tipo_atual = self.tipos_disponiveis.index('pesca')

    def handle_mousebuttondown(self, event):
        mouse_pos = pygame.mouse.get_pos()
        pos_grid = self.grid.tela_para_grid(mouse_pos, self.camera.x, self.camera.y)
        
        if pos_grid:
            # print(f"Mouse click at grid pos: {pos_grid}")  # Debug coord
            if event.button == 1: 
                if self.modo_construcao:
                    if not self.tem_construcao(pos_grid):
                        success = self.construir(
                            pos_grid,
                            self.recursos_gerenciador,
                            "jogador"
                        )
                        # print(f"Construção {'cosntruida com sucesso' if success else 'falha na parte de construção'} at {pos_grid}")
                    else:
                        # print(f"já existe uma construção em {pos_grid}")
                        self.grid.selecionar_celula(mouse_pos, self.camera.x, self.camera.y)
                else:
                    self.grid.selecionar_celula(mouse_pos, self.camera.x, self.camera.y)
            
            elif event.button == 3:  
                self.remover_construcao(pos_grid)

    def atualizar_tile_size(self, tile_size):
        for construcao in self.construcoes:
            construcao.tile_size = tile_size

    def tem_construcao(self, pos_grid):
        x, y = pos_grid

        for construcao in self.construcoes:
            cx, cy = construcao.posicao
            largura, altura = self.tamanho_construcoes[construcao.tipo]

            if cx <= x < cx + largura and cy <= y < cy + altura:
                return True

        return False
    
    def get_construcao(self, pos_grid):
        for construcao in self.construcoes:
            if construcao.posicao == pos_grid:
                return construcao
        return None
    
    def construir(self, pos_grid, recursos, dono="jogador"):
        x, y = pos_grid
        largura, altura = self.tamanho_construcoes[self.tipo_construcao_atual]

        if x + largura > self.cols or y + altura > self.lins:
            return False

        for dy in range(altura):
            for dx in range(largura):
                px = x + dx
                py = y + dy

                if self.tem_construcao((px, py)):
                    return False

                if self.mapa.dados_mapa[py][px] == 3:
                    return False

        if not self.pode_pagar(recursos):
            print("Recursos insuficientes")
            return False

        self.pagar_construcao(recursos)

        nova_construcao = Construcao(
            self.tipo_construcao_atual,
            pos_grid,
            self.camera.tile_size,
            dono=dono
        )

        self.construcoes.append(nova_construcao)
        return True
    
    def remover_construcao(self, pos_grid):
        construcao = self.get_construcao(pos_grid)
        if construcao:
            self.construcoes.remove(construcao)
            return True
        return False
    
    def desenhar_construcoes(self):
        for construcao in self.construcoes:
            construcao.desenhar(self.screen, self.camera.x, self.camera.y)
    
    def desenhar_previa_construcao(self):
        mouse_pos = pygame.mouse.get_pos()
        pos_grid = self.grid.tela_para_grid(mouse_pos, self.camera.x, self.camera.y)

        if pos_grid and not self.tem_construcao(pos_grid):
            x = int(pos_grid[0] * self.camera.tile_size - self.camera.x)
            y = int(pos_grid[1] * self.camera.tile_size - self.camera.y)

            imagem = self.imagens_previa.get(self.tipo_construcao_atual)

            largura_tiles, altura_tiles = self.tamanho_construcoes[self.tipo_construcao_atual]

            largura_px = int(self.camera.tile_size * largura_tiles)
            altura_px = int(self.camera.tile_size * altura_tiles)

            if imagem:
                key = (self.tipo_construcao_atual, self.camera.tile_size)

                if key not in self.cache_previa:
                    self.cache_previa[key] = pygame.transform.scale(
                        imagem,
                        (largura_px, altura_px)
                    )

                img_escalada = self.cache_previa[key]
                img_escalada.set_alpha(150)
                self.screen.blit(img_escalada, (x, y))
                # se a imagem falhar
            else:
                cor = self.cores_previa.get(self.tipo_construcao_atual, (200, 200, 200, 120))

                surface = pygame.Surface(
                    (largura_px, altura_px),
                    pygame.SRCALPHA
                )
                surface.fill(cor)

                self.screen.blit(surface, (x, y))

            pygame.draw.rect(
                self.screen,
                (255, 255, 0),
                (x, y, largura_px, altura_px),
                2
            )

    def get_construcoes_por_tipo(self, dono=None):
        counts = {}

        for c in self.tipos_disponiveis:
            counts[c] = 0

        for construcao in self.construcoes:

            if dono is not None and construcao.dono != dono:
                continue

            if construcao.tipo in counts:
                counts[construcao.tipo] += 1

        return counts

    def update(self):
        self.desenhar_construcoes()
        if self.modo_construcao:
            self.desenhar_previa_construcao()

    def pode_pagar(self, gerenciador):
        custo = self.custos[self.tipo_construcao_atual]
        recursos = gerenciador.get_recursos()

        for recurso, valor in custo.items():
            if recursos.get(recurso, 0) < valor:
                return False

        return True

    def pagar_construcao(self, gerenciador):
        custo = self.custos[self.tipo_construcao_atual]

        for recurso, valor in custo.items():
            gerenciador.consumir(recurso, valor)