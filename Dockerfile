FROM python:3.12-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    supervisor \
  && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia e instala dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o restante do código
COPY . .

# Cria pasta de logs
RUN mkdir -p /app/logs

# Aplica permissão total
RUN chmod -R 777 /app

# Copia configuração do supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Exponha as portas
EXPOSE 5000 8501 8502

# Inicia o supervisord
CMD ["supervisord", "-n"]
