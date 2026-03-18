import os

class MapaGenerator:
    def __init__(self):
        # Localiza a pasta onde os arquivos .txt estão (mesma pasta deste script)
        self.diretorio_base = os.path.dirname(__file__)

    def carregar_matriz(self, id_mapa):
        nome_arquivo = f"./maps/mapa{id_mapa}.txt"
        caminho = os.path.join(self.diretorio_base, nome_arquivo)
        
        matriz = []
        try:
            with open(caminho, "r") as f:
                for linha in f:
                    # Converte "1 2 1" em [1, 2, 1]
                    valores = [int(n) for n in linha.split()]
                    if valores:
                        matriz.append(valores)
            return matriz
        except FileNotFoundError:
            print(f"Erro: {nome_arquivo} não encontrado. Gerando mapa padrão.")
            return [[1 for _ in range(25)] for _ in range(25)]