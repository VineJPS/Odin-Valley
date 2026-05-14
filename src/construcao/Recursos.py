import pygame
from ..core.Ciclos import Ciclos

class GerenciadorRecursos:
    def __init__(self, sistema_construir, ciclos, dono):
        self.sistema_construir = sistema_construir
        self.ciclos = ciclos
        self.dono = dono

        # Mapeamento tipo construção → recurso
        self.producao = {
            'serraria': 'madeira',
            'mina': 'pedra',
            'fazenda' : 'comida',
            'pesca': 'comida',
            'residencial': 'pessoas'  # ou 'trabalhadores' futuro
        }
        
        self.recursos = {
            'madeira': 100,
            'pedra': 100,
            'comida': 100,
            'ouro': 10,  # manual por agora
            'pessoas': 0
        }
        
        self.acumulator = 0.0  # Para taxa 1/seg

    def update(self, dt):
        self.acumulator += dt / 1000.0  # ms → seg
        # Geração fluida: add fracionada sempre
        counts = self.sistema_construir.get_construcoes_por_tipo(self.dono)
        multiplier = 1.0 if not self.ciclos.is_noite() else 0.3
        
        for tipo, count in counts.items():
            if tipo in self.producao:
                recurso = self.producao[tipo]
                gain_frac = count * multiplier * (dt / 1000.0)  # + por frame
                self.recursos[recurso] += gain_frac
                if gain_frac >= 1.0:  # Log só ganhos significativos
                    print(f"+{int(gain_frac)} {recurso} de {count} {tipo} (x{multiplier:.1f})")
        
        self.acumulator = 0.0  # Reset pra compatibilidade, mas fracionado agora

    def gerar_recursos(self):
        # Count construções por tipo
        counts = self.sistema_construir.get_construcoes_por_tipo(self.dono)
        
        multiplier = 1.0 if not self.ciclos.is_noite() else 0.3
        
        for tipo, count in counts.items():
            if tipo in self.producao:
                recurso = self.producao[tipo]
                gain = int(count * multiplier)
                if gain > 0:
                    self.recursos[recurso] += gain
                    print(f"+{gain} {recurso} de {count} {tipo} (x{multiplier:.1f} {'dia' if multiplier==1.0 else 'noite'})")

    def get_recursos(self):
        return self.recursos.copy()

    def consumir(self, recurso, qtd):
        if recurso in self.recursos and self.recursos[recurso] >= qtd:
            self.recursos[recurso] -= qtd
            return True
        return False
