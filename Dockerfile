# Usa una imagen base de Python
FROM python:3.11

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo de requerimientos al contenedor
COPY requirements.txt /app/

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido del directorio actual al contenedor en /app
COPY . /app/

# Expone el puerto 8000 (o el puerto que estés utilizando para tu aplicación)
EXPOSE 8000

# Comando para ejecutar la aplicación FastAPI
CMD ["uvicorn", "api.main:app", "--host", "127.0.0.1", "--port", "8080"]