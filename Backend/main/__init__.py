import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


api = Api()
#Inicializar SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    load_dotenv()
    if not os.path.exists(os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME')):
        os.mknod(os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME'))

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #Url de configuración de base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME')
    db.init_app(app)

    import main.resources as resources
    api.add_resource(resources.UsuariosResource, '/usuarios')
    api.add_resource(resources.UsuarioResource, '/usuario/<id>')
    api.add_resource(resources.PoemasResource, '/poemas')
    api.add_resource(resources.PoemaResource, '/poema/<id>')
    api.add_resource(resources.CalificacionesResource, '/calificaciones')
    api.add_resource(resources.CalifiacionResource, '/calificacion/<id>')
    api.init_app(app)
    #Retornar aplicación inicializada
    return app
