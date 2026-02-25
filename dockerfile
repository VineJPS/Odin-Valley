FROM python:3

# Instala dependências de sistema para o Pygame e interfaces gráficas
RUN apt-get update && apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho dentro do container
WORKDIR /usr/src/app

# Copia e instala as bibliotecas primeiro (melhora o cache do Docker)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos do seu PC para dentro do WORKDIR no container
COPY . .

# Comando para iniciar o servidor do Django
# Usamos 0.0.0.0 para que o container aceite conexões externas
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]