from flask import Blueprint, render_template
from models import Profile

# Creamos el Blueprint para las rutas relacionadas con los usuarios
user_bp = Blueprint('user', __name__)

@user_bp.route('/users')
def list_users():
    """
    Obtiene todos los perfiles de la base de datos y los muestra en una página.
    Se ordena por reputación de forma descendente para mostrar a los usuarios más activos primero.
    """
    # Consultamos la base de datos para obtener todos los perfiles
    all_profiles = Profile.query.order_by(Profile.reputation.desc()).all()
    
    # Renderizamos una nueva plantilla y le pasamos la lista de perfiles
    return render_template('usuarios.html', profiles=all_profiles)
