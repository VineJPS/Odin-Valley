import pygame

class Mapa:
    def __init__(self, id_mapa=1, tile_size=250):
        self.tile_size = tile_size
        self.dados_mapa = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 2, 1],
            [1, 2, 3, 2, 3, 2, 1],
            [1, 2, 2, 2, 2, 2, 1],
            [1, 1, 1, 1, 1, 1, 1],
        ]
        
        # O dicionário com os caminhos para as imagens
        self.biomas = {
            1: "assets/img/grama.png",
            2: "assets/img/terra.png",
            3: "assets/img/neve.png"
        }
        
        self.tiles = self._configurar_tiles()

    def _configurar_tiles(self):
        biblioteca = {}
        
        for id_tile, caminho in self.biomas.items():
            try:
                # Carrega, otimiza e redimensiona
                img = pygame.image.load(caminho).convert_alpha()
                img = pygame.transform.scale(img, (self.tile_size, self.tile_size))
                biblioteca[id_tile] = img
            except:
                # Se a imagem faltar, cria um bloco colorido de segurança
                fallback = pygame.Surface((self.tile_size, self.tile_size))
                cores = {1: (0, 255, 0), 2: (139, 69, 19), 3: (255, 255, 255)}
                fallback.fill(cores.get(id_tile, (255, 0, 255)))
                biblioteca[id_tile] = fallback
                
        return biblioteca

    def draw(self, superficie):
        for linha_index, linha in enumerate(self.dados_mapa):
            for coluna_index, id_tile in enumerate(linha):
                x = coluna_index * self.tile_size
                y = linha_index * self.tile_size
                
                imagem = self.tiles.get(id_tile)
                if imagem:
                    superficie.blit(imagem, (x, y))