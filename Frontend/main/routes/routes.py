from flask import Blueprint, redirect, url_for, render_template, request, Response, make_response
import requests
import json


app = Blueprint('app', __name__, url_prefix='/')

@app.route('/')
def index():
    api_url = "http://127.0.0.1:6000/poemas"

    data = { "page": 1,"per_page" : 10 }

    jwt = request.cookies.get("acces_token")

    headers = {"Content-Type" : "application/json", "Authorization":"Bearer {}".format(jwt)}

    print (jwt)

    response = requests.get(api_url, json=data, headers=headers)

    print(response.status_code)

    print(response.text)

    poemas = json.loads(response.text)

    print (poemas)
    
    return render_template('vista_principal.html')

@app.route('/perfil')
def perfil():
    return render_template('mi_perfil.html')

@app.route('/view-poem')
def view_poem():
    return render_template('ver_poema.html')

@app.route('/upload-poem')
def upload_poem():
    return render_template('subir_poema.html')

@app.route('/login')
def login():
    
    api_url = "http://127.0.0.1:6000/auth/login"

    data = {"email": "danilos@mail.com", "contraseña": "1234"}

    headers = {"Content-Type": "application/json"}

    response = requests.post(api_url, json=data, headers=headers)
    
    print(response.status_code)
    print(response.text)

    token = json.loads(response.text)
    token = token["access_token"]
    print(token)

    resp = make_response(render_template("inicio_sesion.html"))
    resp.set_cookie("access_token", token)
    return resp
    #return render_template('inicio_sesion.html')
    
@app.route('/user-poems')
def user_poems():
    api_url = "http://127.0.0.1:6000/poemas"

    data = {"page": 1, "per_page": 5}

    jwt = request.cookies.get("access_token")
    print(jwt)

    headers = {"Content-Type": "application/json", "Authorization": "BEARER {}".format(jwt)}

    response = requests.get(api_url, json=data, headers=headers)

    print(response.status_code)

    poemas = json.loads(response.text)

    lista_poemas = poemas["poemas"]
    for poema in lista_poemas:
        print(poema)  
    print(type(lista_poemas))

    return render_template('mis_poemas.html', poemas=lista_poemas)

@app.route('/qualify')
def qualify():
    return render_template('calificar_poema.html')

@app.route('/add-user')
def add_user():
    return render_template('añadir_usuario.html')