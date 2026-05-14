import pygame


class Construcao:
    def __init__(self, tipo, posicao_grid, tile_size, tamanho=(2, 2)):
        self.tipo = tipo
        self.posicao = posicao_grid
        self.tile_size = tile_size
        self.tamanho = tamanho  # (largura_tiles, altura_tiles)

        # cores 
        self.cores = {
            'residencial': (255, 0, 0),
            'serraria': (200, 150, 100),
            'mina': (137, 137, 137),
            'fazenda': (150, 100, 100),
            'pesca': (100, 150, 200),
            'base_jogador' : (80, 80, 200),
            'base_oponente' : (255, 0, 0)
        }

        self.icones = {
            'residencial': 'casa',
            'serraria': 'serraria',
            'mina': 'mina',
            'fazenda': 'fazenda',
            'pesca': 'pesqueiro',
            'base_jogador': 'Sua Base',
            'base_oponente': 'Base Inimiga'
        }

        # sprites
        self.imagens = {
            'residencial': pygame.image.load("assets/img/sprites/construcao/Casa.png").convert_alpha(),
            # 'serraria': pygame.image.load("assets/img/sprites/construcao/...").convert_alpha(),
            # 'mina': pygame.image.load("assets/img/sprites/construcao/...").convert_alpha(),
            # 'fazenda': pygame.image.load("assets/img/sprites/construcao/...").convert_alpha(),
            'pesca': pygame.image.load("assets/img/sprites/construcao/pesqueiro.png").convert_alpha(),
            'base_jogador': pygame.image.load("assets/img/sprites/construcao/basePrincipal.png").convert_alpha(),
            'base_oponente': pygame.image.load("assets/img/sprites/construcao/centro_inimigo.png").convert_alpha()
        }

        self.cache_imagem = {}

    def desenhar(self, surface, cam_x, cam_y):
        x = int(self.posicao[0] * self.tile_size - cam_x)
        y = int(self.posicao[1] * self.tile_size - cam_y)

        largura_tiles, altura_tiles = self.tamanho

        largura_px = int(self.tile_size * largura_tiles)
        altura_px = int(self.tile_size * altura_tiles)

        imagem = self.imagens.get(self.tipo)

        # desenha 
        if imagem:
            key = (self.tipo, int(self.tile_size), self.tamanho)

            if key not in self.cache_imagem:
                self.cache_imagem[key] = pygame.transform.scale(
                    imagem,
                    (largura_px, altura_px)
                )

            surface.blit(self.cache_imagem[key], (x, y))

        # cor
        else:
            cor = self.cores.get(self.tipo, (200, 200, 200))

            pygame.draw.rect(surface, cor, (x, y, largura_px, altura_px))
            pygame.draw.rect(surface, (0, 0, 0), (x, y, largura_px, altura_px), 2)

            try:
                fonte = pygame.font.Font(None, int(self.tile_size * 0.45))

                texto = fonte.render(
                    self.icones.get(self.tipo, '?'),
                    True,
                    (255, 255, 255)
                )

                texto_rect = texto.get_rect(
                    center=(x + largura_px // 2, y + altura_px // 2)
                )

                surface.blit(texto, texto_rect)

            except:
                pass

    def to_dict(self):
        return {
            'tipo': self.tipo,
            'posicao': list(self.posicao),
            'tamanho': list(self.tamanho)
        }

    @classmethod
    def from_dict(cls, data, tile_size):
        return cls(
            data['tipo'],
            tuple(data['posicao']),
            tile_size,
            tuple(data.get('tamanho', [2, 2]))
        )