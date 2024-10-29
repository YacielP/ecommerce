# Usar una imagen base oficial de Python
FROM python:3.9

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo requirements.txt al directorio de trabajo
COPY requeriments.txt /app/

# Instalar las dependencias del proyecto
RUN pip install -r requeriments.txt

# Copiar el resto del código de la aplicación
COPY . /app/

# Exponer el puerto 8000 (el puerto donde Django se ejecuta por defecto)
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
