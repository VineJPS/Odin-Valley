import pygame

class Mapa:
    def __init__(self, largura, altura, id_mapa):
        # Dicionário de biomas/mapas
        self.biomas = {
            1: "assets/img/grama.png",
            2: "assets/img/terra.png",
            3: "assets/img/neve.png"
        }
        
        # Pega o caminho com base no ID
        caminho = self.biomas.get(id_mapa, self.biomas[1])
        
        self.background = pygame.image.load(caminho).convert()
        self.background = pygame.transform.scale(self.background, (largura, altura))

    def draw(self, surface):
        surface.blit(self.background, (0, 0))