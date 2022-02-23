FROM python:3.8-slim-buster

# Directorio
RUN mkdir /code
WORKDIR /code

# Instalando paquetes
RUN apt-get update
RUN apt-get install gunicorn -y
RUN apt install libpq-dev python3-dev gcc -y
RUN apt install unzip

# Instalando librerias
COPY requirements.txt /code/
RUN pip3 install -r requirements.txt

# Archivo de credenciales kaggle
COPY kaggle.json /root/.kaggle/kaggle.json

# Puerto
EXPOSE 80

# Copiar codigo
COPY . .
