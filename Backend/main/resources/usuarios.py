from flask_restful import Resource
from flask import request

USUARIOS = {
    1: {'nombre': 'anon3221'},
    2: {'nombre': '6ixn1ne'},
    3: {'nombre': 'anon232123'}

}

class Usuario(Resource):
    def get(self, id):
        if int(id) in USUARIOS:
            return USUARIOS[int(id)]
        return '', 404
    def delete(self, id):
        if int(id) in USUARIOS:
            del USUARIOS[int(id)]
            return '', 204
        return '', 404

    def put(self, id):
        if int(id) in USUARIOS:
            usuario = USUARIOS[int(id)]
            #Obtengo los datos de la solicitud
            data = request.get_json()
            usuario.update(data)
            return usuario, 201
        return '', 404


class Usuarios(Resource):
    def get(self):
        return USUARIOS
    def post(self):
        usuario = request.get_json()
        id = int(max(USUARIOS.keys())) + 1
        USUARIOS[id] = usuario
        return USUARIOS[id], 201
