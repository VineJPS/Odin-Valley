# Salve este arquivo EXATAMENTE com o nome: test_game.py
import pygame
import pytest

def test_pygame_init():
    # Testa se o pygame inicializa corretamente
    pygame.init()
    assert pygame.get_init() == True
    pygame.quit()

def test_screen_creation():
    # Testa se conseguimos casdfrsdfsadfsadfiar uma superfície de vídeo no XVFB
    pygame.init()
    # Ajustei para 640 para bater com o assert abaixo
    screen = pygame.display.set_mode((640, 480)) 
    assert screen.get_width() == 640
    pygame.quit()