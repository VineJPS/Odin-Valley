import pygame
import sys

# 1. Inicializa o Pygame
pygame.init()

# 2. Configura a janela (Largura, Altura)
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Odin Valley - Teste Docker")

# Cores
VERDE_ODIN = (34, 139, 34)
BRANCO = (255, 255, 255)

# Fonte para escrever na tela
font = pygame.font.SysFont("Arial", 36)

# 3. Loop Principal (O que mantém o container vivo)
running = True
while running:
    # Trata eventos (clicar no X, teclado, etc)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Preenche o fundo
    screen.fill(VERDE_ODIN)

    # Desenha um texto na tela
    texto = font.render("Odin Valley está rodando no Docker!", True, BRANCO)
    screen.blit(texto, (150, 250))

    # Atualiza o frame
    pygame.display.flip()

# 4. Finaliza o programa corretamente
pygame.quit()
sys.exit()