# Usar una imagen de Python con las dependencias correctas
FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

# Crear un directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto
COPY . /app

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Instalar los navegadores de Playwright
RUN playwright install

# Exponer el puerto 8080 (Railway usa este por defecto)
EXPOSE 8080

# Comando para iniciar el servidor
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
