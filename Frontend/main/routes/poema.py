from flask import Blueprint, redirect, url_for, render_template


poema = Blueprint('poema', __name__, url_prefix='/poema')

@poema.route('/view/<int:id>')
def view(id):
    return render_template('ver_poema.html')

@poema.route('/subir')
def create():
    return render_template('subir_poema.html')