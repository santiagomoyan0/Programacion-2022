from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UsuarioModel

"""USUARIOS = {
    1: {'nombre': 'anon3221'},
    2: {'nombre': '6ixn1ne'},
    3: {'nombre': 'anon232123'}
} """

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
        usuarios = db.session.query(UsuarioModel).all()
        return jsonify([usuario.to_json_short() for usuario in usuarios])

    """
            list_prof = []
            for professor in professors:
                list_prof.append(professor.to_json())
            return jsonify(list_prof)
    """

    def post(self):
        usuario = UsuarioModel.from_json(request.get_json())
        db.session.add(usuario)
        db.session.commit()
        return usuario.to_json(), 201

