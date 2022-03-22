#Instalar python3-venv para poder manejar entornos virtuales
#Importar Flask
from flask import Flask
#Importar librería os
import os
#Importar DotEnv para manejar variables de entorno
from dotenv import load_dotenv

#Cargar variables de entorno de archivo .env
load_dotenv()
#Inicializar aplicación Flask
app = Flask(__name__)

#Verificar que el script se este ejecutando directamente
if __name__ == '__main__':
    #Correr servidor web
    #Debug: Si está activado muestra mensajes de error y se reinicia al encontrar cambios
    #Port: Puerto en el que va a correr el servicio. Obtenido de las variables de entorno
    app.run(debug = True, port = os.getenv("PORT"))
