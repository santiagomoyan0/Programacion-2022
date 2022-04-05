import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
import main.resources as resources

api = Api()
#Método que inicializará todos los módulos y devolverá la aplicación
def create_app():
    #Inicializar Flask
    app = Flask(__name__)
    #Cargar variables de entorno
    load_dotenv()
    api.add_resource(resources.UsuariosResource, '/usuarios')
    api.add_resource(resources.UsuarioResource, '/usuario/<id>')
    api.add_resource(resources.PoemasResource, '/poemas')
    api.add_resource(resources.PoemaResource, '/poema/<id>')
    api.add_resource(resources.CalificacionesResource, '/calificaciones')
    api.add_resource(resources.CalifiacionResource, '/calificacion/<id>')
    api.init_app(app)
    #Retornar aplicación inicializada
    return app
