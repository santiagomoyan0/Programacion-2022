import os
from flask import Flask
from dotenv import load_dotenv

#Método que inicializará todos los módulos y devolverá la aplicación
def create_app():
    #Inicializar Flask
    app = Flask(__name__)
    #Cargar variables de entorno
    load_dotenv()
    #
    #Aquí se inicializarán el resto de los módulos de la aplicación
    #
    #Retornar aplicación inicializada
    return app
