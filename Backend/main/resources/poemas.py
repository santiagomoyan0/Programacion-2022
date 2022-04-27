from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import PoemaModel


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
        page = 1
        per_page = 10
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key =="page":
                    page = int(value)
                if key == "per_page":
                    per_page = int(value)
        poemas = poemas.paginate(page, per_page, True, 30)
        return jsonify({ 'poemas': [poema.to_json() for poema in poemas.items],
                  'total': poemas.total,
                  'pages': poemas.pages,
                  'page': page
                  })

    

   

    def post(self):
        poema = PoemaModel.from_json(request.get_json())
        db.session.add(poema)
        db.session.commit()
        return poema.to_json(), 201