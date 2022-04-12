from .. import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contraseña = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return '< Usuario: %r %r >' % (self.nombre, self.contraseña, self.email, self.rol)
    #Convertir objeto en JSON
    def to_json(self):
        usuario_json = {
            'id': self.id,
            'nombre': str(self.nombre),
            'contraseña': str(self.contraseña),
            'email': str(self.email),
            'rol': str(self.rol)
        }
        return usuario_json

    def to_json_short(self):
        usuario_json = {
            'id': self.id,
            'nombre': str(self.nombre),

        }
        return usuario_json
    @staticmethod
    #Convertir JSON a objeto
    def from_json(usuario_json):
        id = usuario_json.get('id')
        nombre = usuario_json.get('nombre')
        contraseña = usuario_json.get('contraseña')
        return Usuario(id=id,
                    nombre=nombre,
                    contraseña=contraseña,
                    )
