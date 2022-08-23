from flask import Blueprint, redirect, url_for, render_template

main = Blueprint('main', __name__, url_prefix='/')

@main.route('/')
def index():
    return render_template('vista_principal.html')

@main.route('/login')
def login():
    return render_template('inicio_sesion.html')