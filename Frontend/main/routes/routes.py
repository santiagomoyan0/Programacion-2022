from flask import Blueprint, redirect, url_for, render_template, request, Response, make_response, current_app
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

@app.route('/view-poem')
def view_poem():
    return render_template('ver_poema.html')

@app.route('/upload-poem', methods=['GET', 'POST'])
def upload_poem():
    if request.cookies.get('access_token'):
        if request.method == 'POST':
            titulo = request.form['titulo']
            cuerpo = request.form['cuerpo']
            print(titulo)
            print(cuerpo)
            jwt = request.cookies.get("access_token")
            print(jwt)
            id = request.cookies.get("id")
            print(id)
            data = {"usuarioid": id, "titulo": titulo, "cuerpo": cuerpo}
            headers = {"Content-Type" : "application/json", "Authorization": f"Bearer {jwt}"}
            if titulo != "" and cuerpo != "":
                response = requests.post(f'{current_app.config["API_URL"]}/poemas', json=data, headers=headers)
                if response.ok:
                    response = json.loads(response.text)
                    return redirect(url_for('app.index'))
                else:
                    return redirect(url_for('app.upload-poem'))
            else:
                return redirect(url_for('app.upload-poem'))
        else:
            return render_template('subir_poema.html') 
    else:
        return redirect(url_for('app.login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
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
    return render_template('inicio_sesion.html')
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