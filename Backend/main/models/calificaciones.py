from .. import db

class Calificacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuarioid = db.Column(db.Integer, nullable=False)
    poemaid = db.Column(db.Integer, nullable=False)
    puntaje = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return '< Poema: %r %r >' % (self.puntaje, self.comentario, self.usuarioid, self.poemaid)
    #Convertir objeto en JSON
    def to_json(self):
        calificacion_json = {
            'id': self.id,
            'puntaje': str(self.puntaje),
            'comentario': str(self.comentario)
            
        }
        return calificacion_json

    def to_json_short(self):
        calificacion_json = {
            'id': self.id,
            'puntaje': int(self.puntaje),
            'comentario': str(self.comentario),
            'usuarioid': int(self.usuarioid),
            'poemaid': int(self.poemaid)

        }
        return calificacion_json
    @staticmethod
    #Convertir JSON a objeto
    def from_json(calificacion_json):
        id = calificacion_json.get('id')
        usuarioid = calificacion_json.get('usuarioid')
        poemaid = calificacion_json.get('poemaid')
        puntaje = calificacion_json.get('puntaje')
        comentario = calificacion_json.get('comentario')
        return Calificacion(id=id,
                    usuarioid=usuarioid,
                    poemaid=poemaid,
                    puntaje=puntaje,
                    comentario=comentario
                    )
