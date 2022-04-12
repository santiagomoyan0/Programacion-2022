from main import create_app
import os
from main import db

#Llamar a la función y devolver la app
app = create_app()
#Hacer push sobre el contexto de la aplicación
#Esto permite acceder a las propiedades de la aplicación en cualquier parte del sistema
app.app_context().push()

if __name__ == '__main__':
    db.create_all()
    app.run(debug = True, port = os.getenv("PORT"))
