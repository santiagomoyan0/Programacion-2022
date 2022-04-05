from flask_restful import Resource
from flask import request

CALIFICACIONES = {
    1: {'Calificacion': 'Nueve'},
    2: {'Calificacion': 'Ocho'},
    3: {'Calificacion': 'Siete'}

}

class Calificacion(Resource):
    def get(self, id):
        if int(id) in CALIFICACIONES:
            return CALIFICACIONES[int(id)]
        return '', 404

    def delete(self, id):
        if int(id) in CALIFICACIONES:
            del CALIFICACIONES[int(id)]
            return '', 204
        return '', 404

    def put(self, id):
        if int(id) in CALIFICACIONES:
            calificacion = CALIFICACIONES[int(id)]
            #Obtengo los datos de la solicitud
            data = request.get_json()
            calificacion.update(data)
            return calificacion, 201
        return '', 404

class Calificaciones(Resource):
    def get(self):
        return CALIFICACIONES
    def post(self):
        calificacion= request.get_json()
        id = int(max(CALIFICACIONES.keys())) + 1
        CALIFICACIONES[id] = calificacion
        return CALIFICACIONES[id], 201
