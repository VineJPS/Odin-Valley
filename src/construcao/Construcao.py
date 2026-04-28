import pygame

class Construcao:
    def __init__(self, tipo, posicao_grid, tile_size):
        self.tipo = tipo  
        self.posicao = posicao_grid  
        self.tile_size = tile_size
        
        # cores e nomes temporarios para as construções. enquanto n tiver os sprites
        self.cores = {
            'residencial': (255, 0, 0),        
            'serraria': (200, 150, 100),     
            'mina': (137, 137, 137),          
            'pesca': (100, 150, 200)         
        }
        self.icones = {
            'residencial': 'casa',
            'serraria': 'serraria',
            'mina': 'mina',
            'pesca': 'pesqueiro'
        }
        # sprites
        self.imagens = {
            'residencial': pygame.image.load("assets/img/sprites/construcao/Casa.png").convert_alpha(),
            # 'serraria': pygame.image.load("assets/img/sprites/construcao/...").convert_alpha(),
            # 'mina': pygame.image.load("assets/img/sprites/construcao/...").convert_alpha(),
            # 'pesca': pygame.image.load("assets/img/sprites/construcao/...").convert_alpha(),
        }
        self.cache_imagem = {}
        
        
    def desenhar(self, surface, cam_x, cam_y):
        x = int(self.posicao[0] * self.tile_size - cam_x)
        y = int(self.posicao[1] * self.tile_size - cam_y)

        imagem = self.imagens.get(self.tipo)

        if imagem:
            key = (self.tipo, int(self.tile_size))

            if key not in self.cache_imagem:
                self.cache_imagem[key] = pygame.transform.scale(
                    imagem,
                    (int(self.tile_size), int(self.tile_size))
                )

            surface.blit(self.cache_imagem[key], (x, y))

        # caso a imagem falhe
        else:
            cor = self.cores.get(self.tipo, (200, 200, 200))

            pygame.draw.rect(surface, cor, (x, y, self.tile_size, self.tile_size))
            pygame.draw.rect(surface, (0, 0, 0), (x, y, self.tile_size, self.tile_size), 2)

            try:
                fonte = pygame.font.Font(None, int(self.tile_size * 0.4))
                texto = fonte.render(self.icones.get(self.tipo, '?'), True, (255, 255, 255))
                texto_rect = texto.get_rect(center=(x + self.tile_size//2, y + self.tile_size//2))
                surface.blit(texto, texto_rect)
            except:
                pass


    def to_dict(self):
        return {'tipo': self.tipo, 'posicao': self.posicao}

    @classmethod
    def from_dict(cls, data, tile_size):
        return cls(data['tipo'], data['posicao'], tile_size)
