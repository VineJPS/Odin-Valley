import pygame
import json

class DialogueSystem:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        
        # Fontes
        self.font_nome = pygame.font.SysFont("Arial", 20, bold=True)
        self.font_texto = pygame.font.SysFont("Arial", 18)
        self.font_aviso = pygame.font.SysFont("Arial", 14, italic=True) # Fonte menor para o aviso
        
        self.dialogues = []
        self.current_index = 0
        self.active = False

        # Animação de Digitação
        self.texto_visivel = ""
        self.char_index = 0
        self.last_update = 0
        self.velocidade_texto = 30  # milissegundos por letra
        
        # Configurações da Caixa
        self.rect = pygame.Rect(50, 450, 700, 150)
        self.rect.center = (self.width // 2, self.height - 100)
        self.sprites_cache = {}
        
        # Animação do Sprite
        self.frame_timer = 0
        self.current_frame = 0

        # Overlay
        self.overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 150))  # Preto com transparência (150/255)

    def load_dialogue(self, file_path, key):
        with open(f"src/dialogos/{file_path}", 'r', encoding='utf-8') as f:
            self.dialogues = json.load(f)[key]
        self.current_index = 0
        self.active = True

        self.texto_visivel = ""
        self.char_index = 0
        self.last_update = pygame.time.get_ticks()

    def draw(self):
        if not self.active:
            return
        
        # Escurece o fundo
        self.screen.blit(self.overlay, (0, 0))
        
        info = self.dialogues[self.current_index]

        # --- Animação do Sprite ---
        if pygame.time.get_ticks() - self.frame_timer > 1000:
            self.current_frame = 1 if self.current_frame == 0 else 0
            self.frame_timer = pygame.time.get_ticks()

        # 1. Desenha a Caixa
        pygame.draw.rect(self.screen, (40, 30, 30), self.rect, border_radius=12)
        pygame.draw.rect(self.screen, (200, 180, 50), self.rect, 3, border_radius=12)

        # 2. Desenha o Sprite
        nome_base = info['sprite']
        frames = [f"{nome_base}-1.png", f"{nome_base}-2.png"]
        
        for f_nome in frames:
            if f_nome not in self.sprites_cache:
                try:
                    img = pygame.image.load(f_nome).convert_alpha()
                    self.sprites_cache[f_nome] = pygame.transform.scale(img, (100, 100))
                except:
                    temp = pygame.Surface((100, 100)); temp.fill((100, 100, 100))
                    self.sprites_cache[f_nome] = temp

        sprite_atual = self.sprites_cache[frames[self.current_frame]]
        sprite_rect = sprite_atual.get_rect()
        sprite_rect.center = (
            self.rect.x + 65,  # metade da área do sprite (ajuste fino)
            self.rect.y + self.rect.height // 2
        )

        self.screen.blit(sprite_atual, sprite_rect)

        # 3. Textos Principais
        texto_completo = info['texto']

        agora = pygame.time.get_ticks()
        if agora - self.last_update > self.velocidade_texto:
            if self.char_index < len(texto_completo):
                self.char_index += 1
                self.texto_visivel = texto_completo[:self.char_index]
                self.last_update = agora

        cor_do_nome = info.get('cor_nome', (255, 255, 0))
        surf_nome = self.font_nome.render(info['nome'], True, cor_do_nome)

        largura_max = self.rect.width - 150  # espaço disponível (ajuste fino)
        linhas = self.quebrar_linhas(self.texto_visivel, largura_max)

        y_offset = 0
        for linha in linhas:
            surf = self.font_texto.render(linha, True, (255, 255, 255))
            self.screen.blit(surf, (self.rect.x + 130, self.rect.y + 55 + y_offset))
            y_offset += 25  # espaço entre linhas
        
        self.screen.blit(surf_nome, (self.rect.x + 130, self.rect.y + 15))

        # --- 4. MENSAGEM DE AVISO (Canto inferior direito) ---
        texto_aviso = "Aperte [Espaço] para continuar"
        # O efeito de piscar (opcional): só desenha se o tempo for par
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            surf_aviso = self.font_aviso.render(texto_aviso, True, (180, 180, 180))
            
            # Cálculo da posição: largura da caixa - largura do texto - margem
            pos_x = self.rect.right - surf_aviso.get_width() - 15
            pos_y = self.rect.bottom - surf_aviso.get_height() - 10
            
            self.screen.blit(surf_aviso, (pos_x, pos_y))

    def next_message(self):
        texto_completo = self.dialogues[self.current_index]['texto']
        
        if self.char_index < len(texto_completo):
            # Completa instantaneamente
            self.char_index = len(texto_completo)
            self.texto_visivel = texto_completo
        else:
            # Vai pro próximo diálogo
            self.current_index += 1
            
            if self.current_index >= len(self.dialogues):
                self.active = False
            else:
                # Reset para o próximo texto
                self.char_index = 0
                self.texto_visivel = ""
                self.last_update = pygame.time.get_ticks()
    
    def quebrar_linhas(self, texto, largura_max):
        palavras = texto.split(' ')
        linhas = []
        linha_atual = ""

        for palavra in palavras:
            teste = linha_atual + palavra + " "
            largura, _ = self.font_texto.size(teste)

            if largura <= largura_max:
                linha_atual = teste
            else:
                linhas.append(linha_atual)
                linha_atual = palavra + " "

        linhas.append(linha_atual)
        return linhas