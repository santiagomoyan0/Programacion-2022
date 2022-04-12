from .. import db
from datetime import datetime
class Poema(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuarioid = db.Column(db.Integer, nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    cuerpo = db.Column(db.String(100), nullable=False)
    fecha_hora = db.Column(db.DateTime, nullable=False, default = datetime.now())
    def __repr__(self):
        return '< Poema: %r %r >' % (self.titulo, self.cuerpo, self.fecha_hora)
    #Convertir objeto en JSON
    def to_json(self):
        poema_json = {
            'id': self.id,
            'titulo': str(self.titulo),
            'cuerpo': str(self.cuerpo),
            'fecha_hora': self.fecha_hora.strftime('%Y-%m-%d')
            
        }
        return poema_json

    def to_json_short(self):
        poema_json = {
            'id': self.id,
            'titulo': str(self.titulo),
            'cuerpo': str(self.cuerpo)
            
        }
        return poema_json
    @staticmethod
    #Convertir JSON a objeto
    def from_json(poema_json):
        id = poema_json.get('id')
        usuarioid = poema_json.get('usuarioid')
        titulo = poema_json.get('titulo')
        cuerpo = poema_json.get('cuerpo')
        fecha_hora = datetime.strptime(poema_json.get('fecha_hora'), '%Y-%m-%d')
        return Poema(id=id,
                    usuarioid=usuarioid,
                    titulo=titulo,
                    cuerpo=cuerpo,
                    fecha_hora=fecha_hora
                    )
