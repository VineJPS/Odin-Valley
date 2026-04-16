import pygame
import os
import random

class GerenciadorMusica:
    def __init__(self, pasta_musica="assets/sounds/soundtracks"):
        self.caminho = pasta_musica
        
        # Playlist base (Adicione as Musica aqui)
        self.playlist = {
            "menu": "Menu Music - Ironshield Inn.mp3",
            "song1": "Medieval Tavern Music - Hooded Rogue Inn.mp3",
            "song2": "Medieval Music – Black Wolf's Inn.mp3",
            "song3": "Medieval Minstrel Music – Castle Bard.mp3",
            "song4": "Medieval Minstrel Music - Minstrels of Windsong.mp3",
            "song5": "Fantasy Medieval Music - Sir Morien.mp3"
        }

        self.musica_atual = None

        # Sistema de playlist aleatória
        self.fila = []
        self.tocando_playlist = False

    # Tocar música específica
    def soundtrack(self, musica, volume=0.2, loop=0, fade=2000):
        if musica in self.playlist:
            arquivo = self.playlist[musica]

            # Evita reiniciar a mesma música
            if self.musica_atual == arquivo:
                return

            caminho_completo = os.path.join(self.caminho, arquivo)

            if os.path.exists(caminho_completo):

                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.fadeout(1000)

                pygame.mixer.music.load(caminho_completo)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(loops=loop, fade_ms=fade)

                self.musica_atual = arquivo
        else:
            print(f"Erro: musica '{musica}' não encontrada.")

    def criar_playlist_aleatoria(self):
        self.fila = list(self.playlist.keys())
        random.shuffle(self.fila)
        self.tocando_playlist = True

    def proxima_musica(self):
        if not self.tocando_playlist:
            return

        # Se acabou a lista → recria automaticamente
        if not self.fila:
            self.criar_playlist_aleatoria()

        proxima = self.fila.pop(0)
        self.soundtrack(proxima)

    # Atualizar (chamar no loop do jogo)
    def atualizar(self):
        if self.tocando_playlist and not pygame.mixer.music.get_busy():
            self.proxima_musica()

    def ajustar_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def parar(self):
        pygame.mixer.music.fadeout(1000)
        self.musica_atual = None
        self.tocando_playlist = False