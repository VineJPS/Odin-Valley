# Odin-Valley

##  Tecnologias
* **Backend:** Python
* **Infraestrutura:** Docker & Docker Compose
* **Banco de Dados:** SQL 

##  Equipe
* **Vinicius** (VineJPS)
* **Renan** (RenanHB1)
* **Matheus** (MatheusMenck)
* **Sthefani** (Sthee2004)

---

##  Iniciando o Projeto
| Etapa | Comando | O que faz? |
| :--- | :--- | :--- |
| **1. Permissão de Vídeo** | `xhost +local:docker` | **(Linux apenas)** Permite que o container abra a janela do jogo na sua tela. |
| **2. Criar Imagem** | `docker-compose build` | Constrói a imagem base instalando Python, SDL e as dependências. |
| **3. Subir o Jogo** | `docker-compose up` | Inicia o container **Odin-Valley** e executa o `index.py` automaticamente. |
| **4. Rodar Testes** | `docker-compose run --rm app pytest` | Executa a suite de testes (Pytest) para validar o código. |

---

##  Criando o Executavel
| Etapa | Comando | O que faz? |
| :--- | :--- | :--- |
| **1. Permissão de Vídeo** | `xhost +local:docker` | **(Linux apenas)** Permite que o container abra a janela do jogo na sua tela. |
| **2. Subir o Container** | `docker-compose up` | Inicia o container **Odin-Valley** e executa o `index.py` automaticamente. |
| **3. Acessar o container** | `docker-compose exec app bash` | Entra no container onde as bibliotecas estão instaladas. |
| **4. Criar o Executavel** | `python3 build_game.py` | Executa o arquivo **build_game.py** que gera o executável. |
| **5. Abrir o jogo em wine** | `wine Odin-Valley.exe` | Inicia o jogo **Apenas Linux** |

---

## Abrindo PR
Crie uma nova Branch (Atualizada) a partir da main com os prefixos "feature" criação de algo novo ou "fix" correção de bugs. EX feature/adicao-zoom || fix/correcao-zoom

##  Solução de Problemas

Se encontrar erros de execução ou de bibliotecas, utilize os comandos de manutenção abaixo:

### 1. Reinstalar tudo do zero (Build sem Cache)
Se você alterou o `requirements.txt` ou se o Docker estiver dando erro de `ModuleNotFoundError`, force uma reconstrução limpa:
```bash
docker-compose build --no-cache
