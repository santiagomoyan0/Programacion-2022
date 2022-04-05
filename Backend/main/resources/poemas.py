from flask_restful import Resource
from flask import request

POEMAS = {
    1: {'Titulo': 'queue'},
    2: {'Titulo': 'laliga'},
    3: {'Titulo': 'la esperanza'}

}

class Poema(Resource):
    def get(self, id):
        if int(id) in POEMAS:
            return POEMAS[int(id)]
        return '', 404

    def delete(self, id):
        if int(id) in POEMAS:
            del POEMAS[int(id)]
            return '', 204
        return '', 404

    def put(self, id):
        if int(id) in POEMAS:
            poema = POEMAS[int(id)]
            #Obtengo los datos de la solicitud
            data = request.get_json()
            poema.update(data)
            return poema, 201
        return '', 404


class Poemas(Resource):
    def get(self):
        return POEMAS
    def post(self):
        poema= request.get_json()
        id = int(max(POEMAS.keys())) + 1
        POEMAS[id] = poema
        return POEMAS[id], 201
