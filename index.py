import pygame
import sys
from src.core.Engine import Engine

def main():
    pygame.init()
    tela = pygame.display.set_mode((800, 600))
    fonte = pygame.font.SysFont("Arial", 40)
    
    while True:
        tela.fill((30, 30, 30))
        mouse = pygame.mouse.get_pos()
        
        # Define os Retângulos dos Botões
        btn_start = pygame.Rect(300, 200, 200, 60)
        btn_exit = pygame.Rect(300, 300, 200, 60)

        # Desenha Botão Start
        pygame.draw.rect(tela, (50, 150, 50), btn_start, border_radius=10)
        txt_start = fonte.render("Start", True, (255, 255, 255))
        tela.blit(txt_start, txt_start.get_rect(center=btn_start.center))

        # Desenha Botão Exit
        pygame.draw.rect(tela, (150, 50, 50), btn_exit, border_radius=10)
        txt_exit = fonte.render("Exit", True, (255, 255, 255))
        tela.blit(txt_exit, txt_exit.get_rect(center=btn_exit.center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_start.collidepoint(mouse):
                    # Instancia e inicia a Engine apenas ao clicar em Start
                    meu_app = Engine(tela) 
                    meu_app.start()
                if btn_exit.collidepoint(mouse):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

if __name__ == "__main__":
    main()