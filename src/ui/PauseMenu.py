import pygame

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.opcoes = ["Continuar", "Voltar ao menu"]
        self.selecionado = 0
        self.opcoes_selecionada = []

        self.fonte_titulo = pygame.font.Font(None, 60)
        self.fonte_opcao = pygame.font.Font(None, 40)

    def navegar(self, event):
        if event.key == pygame.K_w:
            self.selecionado -= 1
        elif event.key == pygame.K_s:
            self.selecionado += 1

        self.selecionado %= len(self.opcoes)

    def selecionar(self):
        return self.opcoes[self.selecionado]

    def clicar(self, mouse_pos):
        for i, rect in enumerate(self.opcoes_selecionada):
            if rect.collidepoint(mouse_pos):
                return self.opcoes[i]
        return None

    def desenhar(self):
        largura, altura = self.screen.get_size()
        self.opcoes_selecionada = []

        mouse_pos = pygame.mouse.get_pos()

        overlay = pygame.Surface((largura, altura))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        titulo = self.fonte_titulo.render("Jogo Pausado", True, (255, 255, 255))
        self.screen.blit(titulo, (largura // 2 - titulo.get_width() // 2, 150))

        for i, opcao in enumerate(self.opcoes):
            y = 300 + i * 50

            texto = self.fonte_opcao.render(opcao, True, (255, 255, 255))
            rect = texto.get_rect(center=(largura // 2, y))


            if rect.collidepoint(mouse_pos) or i == self.selecionado:
                cor = (255, 200, 0)  # laranja
                self.selecionado = i 
            else:
                cor = (255, 255, 255)

            texto = self.fonte_opcao.render(opcao, True, cor)

            self.screen.blit(texto, rect)
            self.opcoes_selecionada.append(rect)


