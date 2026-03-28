import pygame

class Hud:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # fonte do textp
        self.fonte_controles = pygame.font.Font(None, 24)
        
        # diz se o hud esta na tela
        self.mostrar_controles = True
        
        # Cores
        self.Branco = (255, 255, 255)
        
    def toggle_controles(self):
        self.mostrar_controles = not self.mostrar_controles
        
    def desenhar(self, screen):
        if self.mostrar_controles:
            self._desenhar_menu_controles(screen)
    #Hud dos controles
    def _desenhar_menu_controles(self, screen):
        y_offset = 10
        
        textos = [
            ("CONTROLES:", self.Branco),
            ("WASD / SETAS ou mouse - movimentar camera", self.Branco),
            ("G - Mostrar/Esconder grid", self.Branco),
            ("H - Mostrar/Esconder controles", self.Branco),
            ("ESC - voltar para o menu principal", self.Branco),
            ("Coordenadas: ", self.Branco),
        ]
        
        for texto, cor in textos:
            superficie = self.fonte_controles.render(texto, True, cor)
            screen.blit(superficie, (10, y_offset))
            y_offset += 25



    #Hud das contruções (ainda não implementado)
    def desenhar_controles_construcao(self, surface):
        """Desenha informações dos controles de construção"""
        fonte = pygame.font.Font(None, 20)
        y_offset = 100
        
        controles = [
            "CONTROLES DE CONSTRUÇÃO:",
            "1,2,3,4 - Selecionar tipo de construção",
            "Clique Esquerdo - Construir",
            "Clique Direito - Remover construção",
        ]
        
        for i, texto in enumerate(controles):
            linha = fonte.render(texto, True, (200, 200, 200))
            surface.blit(linha, (10, y_offset + i * 20))