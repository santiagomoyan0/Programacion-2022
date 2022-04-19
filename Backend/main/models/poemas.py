from .. import db
from datetime import datetime
from sqlalchemy import column

class Poema(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuarioid = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    cuerpo = db.Column(db.String(100), nullable=False)
    fecha_hora = db.Column(db.DateTime, nullable=False, default=datetime.now())
    
    usuario = db.relationship('Usuario', back_populates="poemas",uselist=False,single_parent=True)
    calificaciones = db.relationship("Calificacion", back_populates="poema", cascade="all, delete-orphan")


    def __repr__(self):
        return '< Poema: %r %r >' % (self.usuarioid, self.titulo, self.cuerpo, self.fecha_hora)
    #Convertir objeto en JSON
    def to_json(self):
        poema_json = {
            'id': self.id,
            'titulo': str(self.titulo),
            'cuerpo': str(self.cuerpo),
            'usuario': self.usuario.to_json(),
            'fecha_hora': str(self.fecha_hora.strftime("%d-%m-%Y"))
            
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
        return Poema(id=id,
                    usuarioid=usuarioid,
                    titulo=titulo,
                    cuerpo=cuerpo
                    )
