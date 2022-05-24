from flask_restful import Resource
from flask import request, jsonify
from .. import db
from sqlalchemy import func
from datetime import *
from main.models import PoemaModel
from main.models import UsuarioModel
from main.models import CalificacionModel
from main.auth.decoradores import admin_required
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
class Poema(Resource):
    @jwt_required()
    def get(self, id):
        poema = db.session.query(PoemaModel).get_or_404(id)
        return poema.to_json()
    @jwt_required()
    def delete(self, id):
        claims = get_jwt()
        id_usuario = get_jwt_identity()
        poema = db.session.query(PoemaModel).get_or_404(id)
        if "rol" in claims:
            if claims['rol'] == "admin" or id_usuario == int(poema.usuarioid):
                db.session.delete(poema)
                db.session.commit()
                return '', 204
            else:
                return "Este usuario no puede realizar esa acción"

    


class Poemas(Resource):
    @jwt_required(optional=True)
    def get(self):
        poemas = db.session.query(PoemaModel)
        page = 1
        per_page = 10
        claims = get_jwt()
        identify_usuario = get_jwt_identity()
        if identify_usuario:
            if request.get_json():
                filters = request.get_json().items()
                for key, value in filters:
                    if key =="page":
                        page = int(value)
                    if key == "per_page":
                        per_page = int(value)
            poemas = db.session.query(PoemaModel).filter(PoemaModel.usuarioid != identify_usuario)
            poemas = poemas.outerjoin(PoemaModel.calificaciones).group_by(PoemaModel.id).order_by(func.count(PoemaModel.calificaciones))
        else:
            if request.get_json():
                filters = request.get_json().items()
                for key, value in filters:
                        if key == "page":
                            page = int(value)
                        if key == "per_page":
                            per_page = int(value)

                        if key == 'titulo':
                            poemas = poemas.filter(PoemaModel.titulo.like('%'+value+'%'))
                
                        if key == 'usuarioid':
                            poemas = poemas.filter(PoemaModel.usuarioid == value)
                
                        if key == 'fecha_hora[gt]':
                            poemas = poemas.filter(PoemaModel.fecha_hora >= datetime.strptime(value, '%d-%m-%Y'))
                
                        if key == 'fecha_hora[lt]':
                            poemas = poemas.filter(PoemaModel.fecha_hora <= datetime.strptime(value, '%d-%m-%Y'))
                
                        if key == 'username':
                            poemas = poemas.username(PoemaModel.usuario.has(UsuarioModel.username.like('%'+value+'%')))

                        if key == "sort_by":

                            if value == "fecha_hora":
                                poemas = poemas.order_by(PoemaModel.fecha_hora)
            
                            if value == "fecha_hora[desc]":
                                poemas = poemas.order_by(PoemaModel.fecha_hora.desc())
                
                            if value == "calificacion":
                                poemas = poemas.outerjoin(PoemaModel.calificaciones).group_by(PoemaModel.id).order_by(func.mean(CalificacionModel.puntaje))
                    
                            if value == "calificacion[desc]":
                                poemas = poemas.outerjoin(PoemaModel.calificaciones).group_by(PoemaModel.id).order_by(func.mean(CalificacionModel.puntaje).desc())
                    
                            if value == "nombre":
                                poemas = poemas.order_by(PoemaModel.usuario)
                    
                            if value == "nombre[desc]":
                                poemas = poemas.order_by(PoemaModel.usuario.desc())

        poemas = poemas.paginate(page, per_page, True, 30) 
        if "rol" in claims:
            if claims["rol"] == "admin":
                return jsonify({"poemas":[poema.to_json() for poema in poemas.items],
                "total": poemas.total, "pages": poemas.pages, "page": page})
            else:
                return jsonify({"poemas":[poema.to_json() for poema in poemas.items],
                "total": poemas.total, "pages": poemas.pages, "page": page})
            
    

   
    @jwt_required()
    def post(self):
        id_usuario = get_jwt_identity()
        poema = PoemaModel.from_json(request.get_json())
        usuario = db.session.query(UsuarioModel).get_or_404(id_usuario)
        claims = get_jwt()
        if "rol" in claims:
            if claims["rol"] == "poeta":
                if len(usuario.poemas) == 0 or len(usuario.calificaciones) >= 2:
                    poema.usuario_id = id_usuario
                    db.session.add(poema)
                    db.session.commit()
                    return poema.to_json(), 201
                else:
                    return "No hay suficientes calificaciones por parte de este usuario"
            else:
                return "Este usuario no puede realizar esta acción."