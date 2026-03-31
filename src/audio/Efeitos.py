# Crie funções para os efeitos (clique do mouse, barulho da contrução etc) do jogo
import pygame
import os

class GerenciadorEfeitos:
    def __init__(self, pasta_sons="assets/sounds/effects"):
        self.caminho = pasta_sons
        self.efeitos = {}
        self._carregar_biblioteca()

    def _carregar_biblioteca(self):
        # Adicione aqui os nomes dos seus arquivos de efeito
        arquivos = {
            "clique": "buttonMenu.mp3",
        }
        for nome, arq in arquivos.items():
            caminho_completo = os.path.join(self.caminho, arq)
            if os.path.exists(caminho_completo):
                self.efeitos[nome] = pygame.mixer.Sound(caminho_completo)

    # Alterar aqui o volume dos efeitos
    def tocar(self, nome, volume=1):
        if nome in self.efeitos:
            self.efeitos[nome].set_volume(volume)
            self.efeitos[nome].play()