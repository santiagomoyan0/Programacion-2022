from flask import Blueprint, redirect, url_for, render_template

usuario = Blueprint('usuario', __name__, url_prefix='/usuario')


@usuario.route('/view/<int:id>')
def view(id):
    return render_template('mi_perfil.html')
