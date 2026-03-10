import unittest
import pygame
from src.mapa.Mapa import Mapa
from src.mapa.Grid import Grid

class TestProjeto(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Executa uma vez antes de todos os testes (bom para o pygame)"""
        pygame.init()
        pygame.display.set_mode((1, 1), pygame.NOFRAME)

    def test_mapa_loading(self):
        mapa = Mapa(800, 600, 1)
        self.assertIsInstance(mapa.background, pygame.Surface)

    def test_grid_matrix_size(self):
        grid = Grid(800, 600, 20, 15)
        self.assertEqual(len(grid.data), 15)
        self.assertEqual(len(grid.data[0]), 20)

    def test_grid_initial_values(self):
        grid = Grid(800, 600, 20, 15)
        # Verifica se todos os campos começam com 0
        soma = sum(sum(linha) for linha in grid.data)
        self.assertEqual(soma, 0)

if __name__ == "__main__":
    unittest.main()