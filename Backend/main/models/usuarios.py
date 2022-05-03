from .. import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contraseña = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(100), nullable=False)
    poemas = db.relationship("Poema", back_populates="usuario",cascade="all, delete-orphan")
    calificaciones = db.relationship("Calificacion", back_populates="usuario", cascade="all, delete-orphan")
    def __repr__(self):
        return '< Usuario: %r %r >' % (self.nombre, self.contraseña, self.email, self.rol)
    #Convertir objeto en JSON
    def to_json(self):
        usuario_json = {
            'id': self.id,
            'nombre': str(self.nombre),
            #'contraseña': str(self.contraseña),
            #'email': str(self.email),
            #'rol': str(self.rol),
            'num_poemas': len(self.poemas),
            'num_calificaciones': len(self.calificaciones),
            'poemas':[poema.to_json_short() for poema in self.poemas],
            
        }
        return usuario_json

    def to_json_short(self):
        usuario_json = {
            'id': self.id,
            'nombre': str(self.nombre),

        }
        return usuario_json

    def to_json_complete(self):
        poemas = [poema.to_json() for poema in self.poemas]
        calificaciones = [calificacion.to_json() for calificacion in self.calificaciones]
        usuario_json = {
            'id': self.id,
            'name': str(self.name),
            'password': str(self.password),
            'rol': str(self.rol),
            'email': str(self.email),
            'poemas':poemas,
            'calificaciones':calificaciones
        }
        return usuario_json
    @staticmethod
    #Convertir JSON a objeto
    def from_json(usuario_json):
        id = usuario_json.get('id')
        nombre = usuario_json.get('nombre')
        contraseña = usuario_json.get('contraseña')
        email = usuario_json.get('email')
        rol = usuario_json.get('rol')
        return Usuario(id=id,
                    nombre=nombre,
                    contraseña=contraseña,
                    email=email,
                    rol=rol
                    )
