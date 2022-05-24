from xmlrpc.client import TRANSPORT_ERROR
from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import CalificacionModel
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from main.auth.decoradores import admin_required


class Calificacion(Resource):
    @jwt_required(optional=True)
    def get(self, id):
        claims = get_jwt()
        if "rol" in claims:
            if claims["rol"] == "admin":
                calificacion = db.session.query(CalificacionModel).get_or_404(id)
                return calificacion.to_json()
            else:
                calificacion = db.session.query(CalificacionModel).get_or_404(id)
                return calificacion.to_json()
       

    @jwt_required()
    def delete(self, id):
        claims = get_jwt()
        id_usuario = get_jwt_identity()
        calificacion = db.session.query(CalificacionModel).get_or_404(id)
        if "rol" in claims:    
            if claims["rol"] == "admin" or id_usuario == calificacion.usuarioid:
                db.session.delete(calificacion)
                db.session.commit()
                return '', 204
            else:
                return "Este usuario no está autorizado para realizar esta acción."
        
    @jwt_required()
    def put(self,id):

        id_usuario = get_jwt_identity()
        calificacion = db.session.query(CalificacionModel).get_or_404(id)
        if id_usuario == calificacion.usuarioid:
            data = request.get_json().items()
            for key, value in data:
                setattr(calificacion, key, value)
            
            db.session.add(calificacion)
            db.session.commit() 
            return calificacion.to_json(), 201   
        else:
            return "Este usuario no está autorizado para realizar esta acción."
    

class Calificaciones(Resource):
    @jwt_required(optional=True)
    def get(self):
        claims = get_jwt()
        if "rol" in claims:
            if claims["rol"] == "admin":
                calificaciones = db.session.query(CalificacionModel)
                return jsonify([calificacion.to_json() for calificacion in calificaciones])
            else:
                calificaciones = db.session.query(CalificacionModel)
                return jsonify([calificacion.to_json() for calificacion in calificaciones])    
        

    @jwt_required()
    def post(self):
        id_usuario = get_jwt_identity()
        calificacion = CalificacionModel.from_json(request.get_json())
        claims = get_jwt()
        if "rol" in claims:
            if claims['rol'] == "poeta":
                calificacion.usuarioid = int(id_usuario)
                db.session.add(calificacion)
                db.session.commit()
                return calificacion.to_json(), 201
            else:
                return "Este usuario no está autorizado para realizar esta acción."
