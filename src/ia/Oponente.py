import random


class Oponente:
    def __init__(self, sistema_construir):
        self.sistema = sistema_construir
        self.timer = 0
        self.intervalo = 5000  # 5 segundos

        self.base_x = 30
        self.base_y = 15

    def update(self, dt):
        self.timer += dt

        if self.timer >= self.intervalo:
            self.tomar_decisao()
            self.timer = 0

    def tomar_decisao(self):
        tipos = ['residencial', 'serraria', 'mina', 'fazenda', 'pesca']

        tipo = random.choice(tipos)

        tipo_original = self.sistema.tipo_construcao_atual

        self.sistema.tipo_construcao_atual = tipo

        for _ in range(20):
            x = random.randint(self.base_x - 6, self.base_x + 6)
            y = random.randint(self.base_y - 6, self.base_y + 6)

            if self.sistema.construir((x, y)):
                print(f"Oponente construiu {tipo} em {(x, y)}")
                break

        self.sistema.tipo_construcao_atual = tipo_original