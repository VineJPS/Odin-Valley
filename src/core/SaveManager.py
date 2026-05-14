import json
import os

class SaveManager:
    SAVE_PATH = "savegame.json"

    @classmethod
    def existe_save(cls):
        return os.path.exists(cls.SAVE_PATH)


    @classmethod
    def salvar(cls, engine):
        dados = {
            "camera": {
                "x": engine.camera.x,
                "y": engine.camera.y,
                "tile_size": engine.camera.tile_size
            },

            "construcoes": [
                c.to_dict()
                for c in engine.sistema_construir.construcoes
            ],

            "recursos_jogador": engine.recursos_gerenciador.get_recursos(),
            "recursos_oponente": engine.oponente.recursos.get_recursos(),

            "ciclos": engine.ciclos.get_save_data()
        }

        with open(cls.SAVE_PATH, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4)

        # print("Jogo salvo!")

    @classmethod
    def carregar(cls, engine):
        if not os.path.exists(cls.SAVE_PATH):
            print("Nenhum save encontrado.")
            return False

        with open(cls.SAVE_PATH, "r", encoding="utf-8") as f:
            dados = json.load(f)

        # câmera
        engine.camera.x = dados["camera"]["x"]
        engine.camera.y = dados["camera"]["y"]
        engine.camera.tile_size = dados["camera"]["tile_size"]
        engine.camera.tile_alvo = engine.camera.tile_size

        # sincronizar zoom
        engine.grid.tile_size = engine.camera.tile_size
        engine.mapa.tile_size = engine.camera.tile_size
        engine.sistema_construir.atualizar_tile_size(engine.camera.tile_size)

        # construções
        from src.construcao.Construcao import Construcao

        engine.sistema_construir.construcoes = [
            Construcao.from_dict(c, engine.camera.tile_size)
            for c in dados["construcoes"]
        ]

        # recursos
        engine.recursos_gerenciador.recursos = dados["recursos_jogador"]
        engine.oponente.recursos.recursos = dados["recursos_oponente"]

        # ciclos
        engine.ciclos.load_data(dados["ciclos"])

        # Zoom (instavel)
        engine.grid.tile_size = engine.camera.tile_size
        engine.mapa.tile_size = engine.camera.tile_size
        engine.sistema_construir.atualizar_tile_size(engine.camera.tile_size)

        # print("Jogo carregado!")
        return True