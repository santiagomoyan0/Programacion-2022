from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import PoemaModel

"""POEMAS = {
    1: {'Titulo': 'queue'},
    2: {'Titulo': 'laliga'},
    3: {'Titulo': 'la esperanza'}

}"""

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
        poemas = db.session.query(PoemaModel).all()
        return jsonify([poema.to_json_short() for poema in poemas])

    """
            list_prof = []
            for professor in professors:
                list_prof.append(professor.to_json())
            return jsonify(list_prof)
    """


    def post(self):
        poema = PoemaModel.from_json(request.get_json())
        db.session.add(poema)
        db.session.commit()
        return poema.to_json(), 201