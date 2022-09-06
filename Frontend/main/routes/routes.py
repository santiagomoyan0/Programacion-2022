from flask import Blueprint, redirect, url_for, render_template

app = Blueprint('app', __name__, url_prefix='/')

@app.route('/')
def index():
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
    return render_template('inicio_sesion.html')

@app.route('/user-poems')
def user_poems():
    return render_template('mis_poemas.html')

@app.route('/qualify')
def qualify():
    return render_template('calificar_poema.html')

@app.route('/add-user')
def add_user():
    return render_template('añadir_usuario.html')