from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UsuarioModel
from main.models import CalificacionModel
from main.models import PoemaModel
from sqlalchemy import func
from datetime import *
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decoradores import admin_required

class Usuario(Resource):
    def get(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        return usuario.to_json()
    #Eliminar recurso
    def delete(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204
    #Modificar recurso
    def put(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(usuario, key, value)
        db.session.add(usuario)
        db.session.commit()
        return usuario.to_json() , 201


class Usuarios(Resource):
    def get(self):
        page = 1
        per_page = 10
        usuarios = db.session.query(UsuarioModel)
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key =="page":
                    page = int(value)
                if key == "per_page":
                    per_page = int(value)
                
                if key == 'nombre':
                    usuarios = usuarios.filter(UsuarioModel.nombre.like('%'+value+'%'))

                if key == "sort_by":
                    if key == "nombre":
                        usuarios = usuarios.order_by(UsuarioModel.nombre)
    
                    if value == "num_poemas[desc]":
                        usuarios=usuarios.outerjoin(UsuarioModel.poemas).group_by(UsuarioModel.id).order_by(func.count(UsuarioModel.id).desc())
                    
                    if value == "num_poemas":
                        print("Adentro")
                        usuarios=usuarios.outerjoin(UsuarioModel.poemas).group_by(UsuarioModel.id).order_by(func.count(UsuarioModel.id))
                    
                    if value == "num_calificaciones":
                        print("Adentro")
                        usuarios=usuarios.outerjoin(UsuarioModel.calificaciones).group_by(UsuarioModel.id).order_by(func.count(UsuarioModel.id).desc())
                
                  
        usuarios = usuarios.paginate(page, per_page, True, 30)
        
        return jsonify({ 'usuarios': [usuario.to_json() for usuario in usuarios.items],
                  'total': usuarios.total,
                  'pages': usuarios.pages,
                  'page': page
                  })

   

    def post(self):
        usuario = UsuarioModel.from_json(request.get_json())
        db.session.add(usuario)
        db.session.commit()
        return usuario.to_json(), 201

