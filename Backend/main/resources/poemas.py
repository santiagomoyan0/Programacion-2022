from flask_restful import Resource
from flask import request, jsonify
from .. import db
from sqlalchemy import func
from datetime import *
from main.models import PoemaModel
from main.models import UsuarioModel
from main.models import CalificacionModel

class Poema(Resource):
    def get(self, id):
        poema = db.session.query(PoemaModel).get_or_404(id)
        return poema.to_json()

    def delete(self, id):
        poema = db.session.query(PoemaModel).get_or_404(id)
        db.session.delete(poema)
        db.session.commit()
        return '', 204

    


class Poemas(Resource):
    def get(self):
        poemas = db.session.query(PoemaModel)
        page = 1
        per_page = 10
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key =="page":
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
        return jsonify({"poemas":[poema.to_json_short() for poema in poemas.items],
        "total": poemas.total, "pages": poemas.pages, "page": page})

    

   

    def post(self):
        poema = PoemaModel.from_json(request.get_json())
        db.session.add(poema)
        db.session.commit()
        return poema.to_json(), 201