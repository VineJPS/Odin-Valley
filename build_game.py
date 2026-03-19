import PyInstaller.__main__
import os
import sys
import shutil

def build():
    # 1. Configurações base
    main_script = "index.py"
    project_name = "Odin-Valley"
    base_dir = os.path.abspath(os.getcwd())
    
    # Define o separador: Linux (:) ou Windows (;)
    sep = ";" if sys.platform.startswith("win") else ":"

    print(f"--- 🛠️ Gerando Build de Arquivo Único em: {base_dir} ---")

    # 2. O PULO DO GATO:
    # Mapeamos as pastas para que o PyInstaller crie a mesma estrutura 
    # dentro da pasta temporária onde o executável se descompacta.
    # "Caminho_No_Disco{sep}Caminho_Dentro_Do_Exe"
    data_args = [
        f"--add-data={os.path.join(base_dir, 'assets')}{sep}assets",
        f"--add-data={os.path.join(base_dir, 'src/mapa')}{sep}src/mapa"
    ]

    # 3. Argumentos do PyInstaller
    args = [
        main_script,
        f"--name={project_name}",
        "--onefile",        # Garante o arquivo único
        "--noconsole",      # Oculta o terminal
        "--distpath=.",     # Cospe o executável na home do projeto
        "--clean",          # Limpa builds anteriores
        "-y"                # Sobrescreve sem perguntar
    ] + data_args

    try:
        # Executa a criação
        PyInstaller.__main__.run(args)
        
        # 4. LIMPEZA TOTAL: Remove o "lixo" para deixar sua home limpa
        print("\n---  Limpando rastros do processo ---")
        lixo = ["build", f"{project_name}.spec", "index.spec"]
        for item in lixo:
            caminho_lixo = os.path.join(base_dir, item)
            if os.path.exists(caminho_lixo):
                if os.path.isdir(caminho_lixo):
                    shutil.rmtree(caminho_lixo)
                else:
                    os.remove(caminho_lixo)
                print(f"Removido: {item}")

        print(f"\n SUCESSO! O executável '{project_name}' está na sua home.")
        print("Ele foi configurado para simular sua estrutura de pastas internamente.")

    except Exception as e:
        print(f"\n Erro durante o build: {e}")

if __name__ == "__main__":
    build()