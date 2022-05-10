from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import CalificacionModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decoradores import admin_required


class Calificacion(Resource):
    def get(self, id):
        calificacion = db.session.query(CalificacionModel).get_or_404(id)
        return calificacion.to_json()

    def delete(self, id):
        calificacion = db.session.query(CalificacionModel).get_or_404(id)
        db.session.delete(calificacion)
        db.session.commit()

    

class Calificaciones(Resource):
    def get(self):
        calificaciones = db.session.query(CalificacionModel)
        return jsonify([calificacion.to_json() for calificacion in calificaciones])

    def post(self):
        calificacion = CalificacionModel.from_json(request.get_json())
        db.session.add(calificacion)
        db.session.commit()
        return calificacion.to_json(), 201
