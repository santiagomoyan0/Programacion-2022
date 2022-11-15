from flask import Flask, Blueprint, current_app, render_template, make_response, request, redirect, url_for
import requests
import json

app = Blueprint('app', __name__, url_prefix='/')

@app.route('/')
def index():

    api_url = "http://127.0.0.1:6000/poemas"

    data = { "page": 1,"per_page" : 10 }
    
    jwt = request.cookies.get("access_token")

    headers = {"Content-Type" : "application/json", "Authorization":"Bearer {}".format(jwt)}
    print (jwt)

    response = requests.get(api_url, json=data, headers=headers)
    print(response.status_code)
    print(response.text)

    #obtener poemas en json
    poemas = json.loads(response.text)
    print (poemas)

    return render_template('vista_principal.html', poemas = poemas['poemas'])

@app.route('/perfil')
def perfil():
    return render_template('mi_perfil.html')

@app.route('/view-poem/<int:id>', methods=['GET'])
def view_poem(id):
    api_url = f'{current_app.config["API_URL"]}/poema/{id}'
    print("aca esta el", id)
    jwt = request.cookies.get("access_token")
    headers = {f"Content-Type" : "application/json", "Authorization" : "Bearer {}".format(jwt)}
    response = requests.get(api_url, headers=headers)
    poema = json.loads(response.text)
    print(poema)
    return render_template('ver_poema.html', poema = poema)

@app.route('/upload-poem', methods=['GET', 'POST'])
def upload_poem():
    jwt = request.cookies.get("access_token")
    if request.cookies.get('access_token'):
        print("hola")
        if request.method == 'POST':
            titulo = request.form['titulo']
            cuerpo = request.form['cuerpo']
            print(titulo)
            print(cuerpo)
            print(jwt)
            usuarioid = request.cookies.get("id")
            print(usuarioid)
            data = {"usuarioid": usuarioid, "titulo": titulo, "cuerpo": cuerpo}
            headers = {"Content-Type" : "application/json", "Authorization": f"Bearer {jwt}"}
            if titulo != "" and cuerpo != "":
                response = requests.post(f'{current_app.config["API_URL"]}/poemas', json=data, headers=headers)
                if response.ok:
                    response = json.loads(response.text)
                    print(response)
                    return redirect(url_for('app.index'))
                else:
                    return redirect(url_for('app.upload_poem'))
            else:
                return redirect(url_for('app.upload_poem'))
        else:
            return render_template('subir_poema.html', jwt=jwt) 
    else:
        return redirect(url_for('app.login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if (request.method == 'POST'):
        #obtener datos del formulario - Esto lo traigo del HTML con los name de los inputs. 
        email = request.form['email']
        contraseña = request.form['contraseña']
        print(email, contraseña)

        if email != None and contraseña != None: 
            #es la url que utilizamos en insomnia
            api_url = f'{current_app.config["API_URL"]}/auth/login'
            #Envio de token
            data = {"email" : email, "contraseña" : contraseña}
            headers = {"Content-Type" : "application/json"}
            response = requests.post(api_url, json = data, headers = headers) 
            print("login", response)
            if (response.ok): 

                response = json.loads(response.text)
                token = response["access_token"]
                usuarioid = str(response["id"])

                #Guardar el token en las cookies y devuelve la pagina 
                response = make_response(redirect(url_for('app.index')))
                #response = make_response(user_main(jwt=token)) 
                response.set_cookie("access_token", token)
                response.set_cookie("id", usuarioid)
                return response
                #return render_template('login.html')
        return(render_template('inicio_sesion.html', error = "Usuario o contraseña incorrectos"))
    else:
        return render_template('inicio_sesion.html')
    """if request.method == 'POST':
        email= request.form['email']
        contraseña= request.form['contraseña']
        print(email)
        print(contraseña)

        api_url = "http://127.0.0.1:6000/auth/login"

        data = {"email": "danilos@mail.com", "contraseña": "1234"}

        headers = {"Content-Type": "application/json"}

        response = requests.post(api_url, json=data, headers=headers)
        if response.status_code == 200:

            print(response.status_code)
            print(response.text)

            token = json.loads(response.text)
            token = token["access_token"]
            print(token)

            resp = make_response(redirect(url_for('app.index')))
            resp.set_cookie("access_token", token)
            return resp
        else:
            return render_template('inicio_sesion.html')
    return render_template('inicio_sesion.html')"""
@app.route('/user-poems')
def user_poems():

    api_url = "http://127.0.0.1:6000/poemas"

    data = {"page": 1, "per_page": 5}

    jwt = request.cookies.get("access_token")
    print(jwt)

    headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(jwt)}

    response = requests.get(api_url, json=data, headers=headers)

    print(response.status_code)

    poemas = json.loads(response.text)

    poemas = poemas["poemas"]

    return render_template('mis_poemas.html', jwt = jwt, poemas = poemas)

@app.route('/qualify')
def qualify():
    return render_template('calificar_poema.html')

@app.route('/add-user')
def add_user():
    return render_template('añadir_usuario.html')


@app.route('/logout')
def logout():
    #Crear una request de redirección
    req = make_response(redirect(url_for('app.login')))
    #Borrar cookie
    req.delete_cookie("access_token")
    req.delete_cookie("id")
    return req

"""@app.route('/poem/<int:id>/delete')
def delete_poem(id):
    if request.cookies.get('accsess_token'):
        api_url = f'{current_app.config["API_URL"]}/poema/{id}'
        headers = {"Content-Type" : "application/json"}
        response = requests.delete(api_url, headers=headers)
        return response"""