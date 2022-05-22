from .. import jwt
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity
from functools import wraps

#Decorador para restringir el acceso a usuarios admin
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        #Verificar que el JWT es correcto
        verify_jwt_in_request()
        #Obtener claims de adentro del JWT
        claims = get_jwt()
        #Verificar que el rol sea admin
        if claims['rol'] =="admin" :
            #Ejecutar función
            return fn(*args, **kwargs)
        else:
            return 'Only admins can access', 403
    return wrapper
def admin_required_or_poeta_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        id_usuario = verify_jwt_in_request()
        claims = get_jwt()
        if claims['rol'] == "admin" or id_usuario == id:
                return fn(*args, **kwargs)
        else:
            return 'Only admins or poeta can access', 403
    return wrapper

def poeta_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['rol'] == 'poeta':
            return fn(*args, **kwargs)
        else:
            return 'Only poetas can access', 403
       
    return wrapper  


#Define el atributo que se utilizará para identificar el usuario
@jwt.user_identity_loader
def user_identity_lookup(usuario):
    #Definir ID como atributo identificatorio
    return usuario.id

#Define que atributos se guardarán dentro del token
@jwt.additional_claims_loader
def add_claims_to_access_token(usuario):
    claims = {
        'rol': usuario.rol,
        'id': usuario.id,
        'email': usuario.email
    }
    return claims
