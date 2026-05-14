import random
from src.construcao.Recursos import GerenciadorRecursos

class Oponente:
    def __init__(self, sistema_construir):
        self.sistema = sistema_construir
        self.timer = 0
        self.intervalo = 5000

        self.cooldown_falha = 0

        self.base_x = 30
        self.base_y = 15

        self.recursos = GerenciadorRecursos(
            sistema_construir,
            sistema_construir.recursos_gerenciador.ciclos,
            "oponente"
        )

    def update(self, dt):
        self.recursos.update(dt)

        if self.cooldown_falha > 0:
            self.cooldown_falha -= dt
            return

        self.timer += dt

        if self.timer >= self.intervalo:
            self.tomar_decisao()
            self.timer = 0

    def construcoes_existentes(self):
        counts = self.sistema.get_construcoes_por_tipo("oponente")

        return {
            tipo: counts.get(tipo, 0)
            for tipo in ['residencial', 'serraria', 'mina', 'fazenda']
        }

    def escolher_construcao_inicial(self):
        counts = self.construcoes_existentes()

        ordem = [
            'residencial',
            'serraria',
            'mina',
            'fazenda'
        ]

        for tipo in ordem:
            if counts[tipo] == 0:
                return tipo

        return None

    def escolher_construcao(self):
        inicial = self.escolher_construcao_inicial()

        if inicial:
            return inicial

        recursos = self.recursos.get_recursos()

        prioridades = {
            'madeira': 'serraria',
            'pedra': 'mina',
            'comida': 'fazenda',
            'pessoas': 'residencial'
        }

        recurso_critico = min(
            prioridades.keys(),
            key=lambda r: recursos[r]
        )

        return prioridades[recurso_critico]

    def tomar_decisao(self):
        tipo = self.escolher_construcao()

        tipo_original = self.sistema.tipo_construcao_atual
        self.sistema.tipo_construcao_atual = tipo

        construiu = False

        for _ in range(20):
            x = random.randint(self.base_x - 6, self.base_x + 6)
            y = random.randint(self.base_y - 6, self.base_y + 6)

            if self.sistema.construir(
                (x, y),
                self.recursos,
                "oponente"
            ):
                print(f"Oponente construiu {tipo}")
                construiu = True
                break

        if not construiu:
            print("Oponente aguardando recursos...")
            self.cooldown_falha = 10000

        self.sistema.tipo_construcao_atual = tipo_original

        