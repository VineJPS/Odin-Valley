import pygame
from src.mapa.MapaLoader import MapaLoader

class Mapa:
    def __init__(self, id_mapa=1, tile_size=100):
        self.tile_size = tile_size
        
        # Usa o gerador para buscar os dados do arquivo .txt
        self.gerador = MapaLoader()
        self.dados_mapa = self.gerador.carregar_matriz(id_mapa)
        
        # Configura as imagens
        self.biomas = {
            1: "assets/img/terra.png",
            2: "assets/img/grama.jpeg",
            3: "assets/img/agua.png",
            4: "assets/img/areia.png",
            5: "assets/img/terra.png",
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
        self.draw_with_night_effect(superficie, cam_x, cam_y, False, 0.0)

    def draw_with_night_effect(self, superficie, cam_x, cam_y, is_noite, alpha_sombra):
        # Desenha mapa normal primeiro
        tile_size_int = int(self.tile_size)
        largura_t, altura_t = superficie.get_size()

        for l_idx, linha in enumerate(self.dados_mapa):
            for c_idx, id_tile in enumerate(linha):
                x = int(c_idx * tile_size_int - cam_x)
                y = int(l_idx * tile_size_int - cam_y)

                if x < -self.tile_size or y < -self.tile_size:
                    continue
                if x > largura_t or y > altura_t:
                    continue

                tile = self.tiles.get(id_tile)
                superficie.blit(tile, (x, y))

        # Overlay sombra se noite
        if is_noite and alpha_sombra > 0:
            overlay = pygame.Surface((largura_t, altura_t), pygame.SRCALPHA)
            sombra_cor = (*[0]*3, int(255 * alpha_sombra))  # Preto com alpha gradual
            overlay.fill(sombra_cor)
            superficie.blit(overlay, (0, 0))
