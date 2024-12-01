# Base Python 3.11 no Debian Slim
FROM python:3.11-slim

# Atualizar repositórios e instalar dependências necessárias
RUN apt-get update && apt-get install -y \
    zip \
    gcc \
    libffi-dev \
    python3-dev \
    tar \
    wget

# Copiar e instalar o WinRAR
COPY rarlinux-x64-701.tar.gz /tmp/
RUN tar -xzf /tmp/rarlinux-x64-701.tar.gz -C /tmp && \
    mv /tmp/rar/* /usr/local/bin/ && \
    chmod +x /usr/local/bin/rar /usr/local/bin/unrar && \
    rm -rf /tmp/rar /tmp/rarlinux-x64-701.tar.gz

# Configurar diretório de trabalho
WORKDIR /app

# Copiar os arquivos do projeto para o contêiner
COPY . /app

# Instalar dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta para execução local (se necessário)
EXPOSE 5000

# Comando padrão
CMD ["sh"]
