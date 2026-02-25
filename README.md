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

| Etapa | Comando | Descrição |
| :--- | :--- | :--- |
| **1. Imagem** | `docker build -t python-django-pygame .` | Constrói a imagem instalando Python, Django e Pygame. |
| **2. Projeto** | `docker-compose run app django-admin startproject Core .` | Cria os arquivos iniciais do Django na sua máquina local. |
| **3. Banco** | `docker-compose run app python manage.py migrate` | Cria o banco de dados SQLite e as tabelas do sistema. |
| **4. Admin** | `docker-compose run app python manage.py createsuperuser` | (Opcional) Cria seu login para o painel administrativo. |
| **5. Subir** | `docker-compose up` | Inicia o servidor em http://localhost:8000. |

> **Nota para Linux:** Caso os arquivos criados pelo Docker apareçam com um cadeado, rode:  
> `sudo chown -R $USER:$USER .`
