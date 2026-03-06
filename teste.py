# test_game.py
import pygame
import pytest

def test_pygame_init():
    # Testa se o pygame inicializa corretamente no ambiente virtual
    pygame.init()
    assert pygame.get_init() == True
    pygame.quit()

def test_screen_creation():
    # Testa se conseguimos criar uma superfície de vídeo no XVFB
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    assert screen.get_width() == 800
    pygame.quit()