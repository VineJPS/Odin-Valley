# Crie funções para a trilha sonora do jogo
import pygame
import os

class GerenciadorMusica:
    def __init__(self, pasta_musica="assets/sounds/soundtracks"):
        self.caminho = pasta_musica
        # Adicione as musica por aqui
        self.playlist = {
            "menu": "Menu Music - Ironshield Inn.mp3",
            "song1": "Medieval Tavern Music - Hooded Rogue Inn.mp3",
            "song2": "Medieval Music – Black Wolf's Inn.mp3",
            "song3": "Medieval Minstrel Music – Castle Bard.mp3",
            "song4": "Medieval Minstrel Music - Minstrels of Windsong.mp3",
            "song5": "Fantasy Medieval Music - Sir Morien.mp3"
        }
        self.musica_atual = None

    def soundtrack(self, musica, volume=0.2, loop=-1, fade=2000):
        if musica in self.playlist:
            arquivo = self.playlist[musica]
            
            # Evita reiniciar a música se ela já estiver tocando
            if self.musica_atual == arquivo:
                return

            caminho_completo = os.path.join(self.caminho, arquivo)
            
            if os.path.exists(caminho_completo):
                # Se já houver algo tocando, faz um fadeout antes
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.fadeout(1000)
                
                pygame.mixer.music.load(caminho_completo)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(loops=loop, fade_ms=fade)
                self.musica_atual = arquivo
        else:
            print(f"Erro: musica '{musica}' não encontrada na playlist.")

    def ajustar_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def parar(self):
        pygame.mixer.music.fadeout(1000)
        self.musica_atual = None