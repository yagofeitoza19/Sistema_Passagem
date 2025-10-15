# Usar uma imagem base oficial do Python
FROM python:3.9-slim

# Definir o diretório de trabalho no contêiner
WORKDIR /app

# Copiar o arquivo de dependências e instalar
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o conteúdo do diretório atual (incluindo init_db.py)
COPY . .

# Comando para expor a porta que a aplicação vai rodar
EXPOSE 8000

# Comando para iniciar a aplicação com Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]