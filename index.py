import pygame
import sys
from src.core.Engine import Engine
from src.audio.Efeitos import GerenciadorEfeitos
from src.audio.SoundTrack import GerenciadorMusica

def main():
    pygame.init()
    # Pega a resolução real do seu monitor
    info = pygame.display.Info()
    resolucao_nativa = (info.current_w, info.current_h)

    # Atribui a variável com suporte a tela cheia e redimensionamento automático
    tela = pygame.display.set_mode(resolucao_nativa, pygame.FULLSCREEN | pygame.SCALED)
    fonte = pygame.font.SysFont("Arial", 40)

    # Iniciando os gerenciadores de som
    efeitos = GerenciadorEfeitos()
    musica = GerenciadorMusica()

    # Iniciando a Musica do Menu
    musica.soundtrack("menu")

    # Adicionando o background do menu
    bg = pygame.image.load("assets/img/background.png").convert()
    bg = pygame.transform.scale(bg, resolucao_nativa)

    
    while True:
        # Deixando o background atras de todos elemento na tela
        tela.blit(bg, (0, 0))

        mouse = pygame.mouse.get_pos()
        
        # Define os Retângulos dos Botões
        btn_start = pygame.Rect(0, 0, 200, 60)
        btn_option = pygame.Rect(0, 0, 200, 60)
        btn_exit = pygame.Rect(0, 0, 200, 60)

        #Centralizando os botões
        btn_start.center = (info.current_w//2,info.current_h//2)
        btn_option.center = (info.current_w//2,info.current_h//2+100)
        btn_exit.center = (info.current_w//2,info.current_h//2+200)

        # Desenha Botão Start
        pygame.draw.rect(tela, (255, 140, 58), btn_start, border_radius=10)
        txt_start = fonte.render("Start", True, (255, 255, 255))
        tela.blit(txt_start, txt_start.get_rect(center=btn_start.center))

        # Desenha Botão Option
        pygame.draw.rect(tela, (255, 140, 58), btn_option, border_radius=10)
        txt_exit = fonte.render("Option", True, (255, 255, 255))
        tela.blit(txt_exit, txt_exit.get_rect(center=btn_option.center))

        # Desenha Botão Exit
        pygame.draw.rect(tela, (255, 140, 58), btn_exit, border_radius=10)
        txt_exit = fonte.render("Exit", True, (255, 255, 255))
        tela.blit(txt_exit, txt_exit.get_rect(center=btn_exit.center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_start.collidepoint(mouse):
                    efeitos.tocar("clique")
                    musica.soundtrack("song1")
                    # Instancia e inicia a Engine apenas ao clicar em Start
                    meu_app = Engine(tela) 
                    meu_app.start()

                if btn_exit.collidepoint(mouse):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

if __name__ == "__main__":
    main()