import pygame
from src.mapa.MapaGenerator import MapaGenerator

class Mapa:
    def __init__(self, id_mapa=1, tile_size=100):
        self.tile_size = tile_size
        
        # Usa o gerador para buscar os dados do arquivo .txt
        self.gerador = MapaGenerator()
        self.dados_mapa = self.gerador.carregar_matriz(id_mapa)
        
        # Configura as imagens
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
                img = pygame.image.load(caminho).convert_alpha()
                biblioteca[id_tile] = pygame.transform.scale(img, (self.tile_size, self.tile_size))
            except:
                fallback = pygame.Surface((self.tile_size, self.tile_size))
                cores = {1: (34, 139, 34), 2: (139, 69, 19), 3: (255, 255, 255)}
                fallback.fill(cores.get(id_tile, (255, 0, 255)))
                biblioteca[id_tile] = fallback
        return biblioteca

    def draw(self, superficie, cam_x, cam_y):
        largura_t, altura_t = superficie.get_size()

        for l_idx, linha in enumerate(self.dados_mapa):
            for c_idx, id_tile in enumerate(linha):
                x = (c_idx * self.tile_size) - cam_x
                y = (l_idx * self.tile_size) - cam_y
                
                # Culling (Desenha apenas o visível)
                if -self.tile_size < x < largura_t and -self.tile_size < y < altura_t:
                    superficie.blit(self.tiles.get(id_tile), (x, y))