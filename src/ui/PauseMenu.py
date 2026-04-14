import pygame

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.opcoes = ["Continuar", "Voltar ao menu"]
        self.selecionado = 0

        self.fonte_titulo = pygame.font.Font(None, 60)
        self.fonte_opcao = pygame.font.Font(None, 40)

    def navegar(self, event):
        if event.key == pygame.K_UP:
            self.selecionado -= 1
        elif event.key == pygame.K_DOWN:
            self.selecionado += 1

        self.selecionado %= len(self.opcoes)

    def selecionar(self):
        return self.opcoes[self.selecionado]

    def desenhar(self):
        largura, altura = self.screen.get_size()

        overlay = pygame.Surface((largura, altura))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        titulo = self.fonte_titulo.render("PAUSE", True, (255, 255, 255))
        self.screen.blit(titulo, (largura // 2 - titulo.get_width() // 2, 150))

        for i, opcao in enumerate(self.opcoes):
            cor = (255, 255, 0) if i == self.selecionado else (255, 255, 255)

            texto = self.fonte_opcao.render(opcao, True, cor)

            x = largura // 2 - texto.get_width() // 2
            y = 300 + i * 50

            self.screen.blit(texto, (x, y))