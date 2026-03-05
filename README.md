# TropicoGame

##  Tecnologias
* **Backend:** Python / Django
* **Infraestrutura:** Docker & Docker Compose
* **Banco de Dados:** SQL 

##  Devs
* **Vinicius** (VineJPS)
* **Renan** (RenanHB1)
* **Matheus** (MatheusMenck)

---

## Como Rodar o Projeto (Docker)

Siga os passos abaixo para configurar o ambiente e rodar o projeto pela primeira vez.

| Etapa | Comando | O que faz? |
| :--- | :--- | :--- |
| 1. Criar Imagem | `docker build -t python-pygame .` | Lê o seu Dockerfile e instala o Python, Django e as bibliotecas de sistema. |
| 2. Criar Container | `docker run -it --rm --name tropico-game python-pygame` | Usa a imagem para gerar os arquivos do projeto (manage.py, etc.) na sua pasta real. |
| 3. Da permissão para escrever na tela | xhost +local:docker | permissão de escrita. |
| 4. Subir | `docker-compose up` | Liga o servidor e deixa o site disponível em http://localhost:8000. |

> **Nota para Linux:** Caso os arquivos criados pelo Docker apareçam com um cadeado, rode:
> 
> `sudo chown -R $USER:$USER .`
