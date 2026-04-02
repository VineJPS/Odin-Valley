import pygame
import os 

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
            ("B - alternar entre o modo de contrução/visualização ", self.Branco),
            ("ESC - voltar para o menu principal", self.Branco),
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
            "CONTROLES DO MODO CONSTRUÇÃO:",
            "1,2,3,4 - Selecionar tipo de construção",
            "Clique Esquerdo - Construir",
            "Clique Direito - Remover construção",
            "B - alternar entre o modo de contrução/visualização",
            "ESC - voltar para o menu principal"
        ]
        
        for i, texto in enumerate(controles):
            linha = fonte.render(texto, True, (200, 200, 200))
            surface.blit(linha, (10, y_offset + i * 20))


# Hud dos Recursos
class recursoHud:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 20, bold=True)
        
        self.largura_box = 150
        self.altura_box = 40 
        self.margem_interna = 8
        self.espacamento = 8
        self.tamanho_img = 24

        self.elementos = [
            # {"nome": "Pessoas", "valor": 100, "cor": (100, 149, 237),  "img": pygame.transform.scale(pygame.image.load("assets/img/icones/madeira.png"), (self.tamanho_img, self.tamanho_img))},
            {"nome": "Madeira", "valor": 100, "cor": (116, 68, 40),  "img": pygame.transform.scale(pygame.image.load("assets/img/icones/madeira.png"), (self.tamanho_img, self.tamanho_img))},
            {"nome": "Pedra", "valor": 100, "cor": (128, 128, 128),  "img": pygame.transform.scale(pygame.image.load("assets/img/icones/pedra.png"), (self.tamanho_img, self.tamanho_img))},
            {"nome": "Comida", "valor": 100, "cor": (227, 143, 93),  "img": pygame.transform.scale(pygame.image.load("assets/img/icones/comida.png"), (self.tamanho_img, self.tamanho_img))},
            {"nome": "Ouro", "valor": 100, "cor": (254, 198, 2),  "img": pygame.transform.scale(pygame.image.load("assets/img/icones/ouro.png"), (self.tamanho_img, self.tamanho_img))},
        ]

    def exibir_recursos(self):
        total_elementos = len(self.elementos)
        altura_total_hud = (self.altura_box + self.espacamento) * total_elementos
        
        # Posição inicial Y (canto inferior)
        pos_y_inicial = self.screen.get_height() - altura_total_hud - 20
        x = 20

        for i, item in enumerate(self.elementos):
            y = pos_y_inicial + (i * (self.altura_box + self.espacamento))

            # 75% de 255 (alpha máximo) é aproximadamente 191
            alpha = 191 
            
            # pygame.SRCALPHA garante que o canal alpha funcione (transparencia)
            surface_box = pygame.Surface((self.largura_box, self.altura_box), pygame.SRCALPHA)
            
            # O fundo do retangulo fica com a cor definida
            cor_com_alpha = (*item["cor"], alpha)
            pygame.draw.rect(surface_box, cor_com_alpha, surface_box.get_rect(), border_radius=100)
            
            pygame.draw.rect(surface_box, (0,0,0, alpha), surface_box.get_rect(), 2, border_radius=100)

            self.screen.blit(surface_box, (x, y))

            # Renderizar Imagem (Lado Esquerdo)
            img_recurso = item["img"]
            ponto_y_img = y + (self.altura_box // 2) - (self.tamanho_img // 2)
            self.screen.blit(img_recurso, (x+10 + self.margem_interna, ponto_y_img))

            # Renderizar Valor (Lado Direito)
            # Usamos cor branca para o texto para contrastar bem com fundos coloridos
            txt_valor = self.font.render(str(item["valor"]), True, (255,255,255))
            largura_valor = txt_valor.get_width()
            altura_valor = txt_valor.get_height()
            
            # Centraliza verticalmente o texto e encosta na direita
            ponto_y_txt = y + (self.altura_box // 2) - (altura_valor // 2)
            ponto_x_txt = x + self.largura_box - largura_valor - self.margem_interna
            
            self.screen.blit(txt_valor, (ponto_x_txt-10, ponto_y_txt))


# Botões de Gerenciamento no meio inferior da tela
class GerenciamentoHud:
    def __init__(self, x_centro, y_centro, raio, nome_img, letra, tamanho_arq):
        margem_inferior=40
        self.pos_x = x_centro // 2
        self.pos_y = y_centro - raio - margem_inferior
        self.raio = raio
        self.cor_circulo = (255, 175, 1, 171)
        self.tamanho_arq = tamanho_arq

        PASTA_IMG = "assets/img/icones" 
        caminho_completo = os.path.join(PASTA_IMG, nome_img)
        
        img_original = pygame.image.load(caminho_completo).convert_alpha()
        tamanho_img = int(raio * self.tamanho_arq)
        self.imagem = pygame.transform.scale(img_original, (tamanho_img, tamanho_img))

        self.img_rect = self.imagem.get_rect(center=(self.pos_x, self.pos_y))
        
        # 2. Configurar o Texto
        self.fonte = pygame.font.SysFont("Arial", 18, bold=False)
        self.texto_surf = self.fonte.render(letra, True, (0, 0, 0))
        self.texto_rect = self.texto_surf.get_rect(center=(self.pos_x, self.pos_y + self.raio - 15))

    def desenhar_circulo(self, tela):
        surf_circulo = pygame.Surface((self.raio*2, self.raio*2), pygame.SRCALPHA)
        pygame.draw.circle(surf_circulo, self.cor_circulo, (self.raio, self.raio), self.raio)
        tela.blit(surf_circulo, (self.pos_x - self.raio, self.pos_y - self.raio))

        tela.blit(self.imagem, self.img_rect)
        tela.blit(self.texto_surf, self.texto_rect)