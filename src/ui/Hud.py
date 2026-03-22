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