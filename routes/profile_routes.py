from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db
from models import Profile
from flask_login import login_required, current_user

# Creamos el Blueprint para las rutas de perfiles
profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile')
@login_required # ¡Ruta protegida! Solo usuarios con sesión iniciada pueden ver su perfil.
def view_profile():
    """
    Muestra la página de perfil del usuario actualmente autenticado.
    'current_user' es proporcionado por Flask-Login y contiene los datos del perfil.
    """
    return render_template('perfil.html', user_profile=current_user)


@profile_bp.route('/profile/edit', methods=['POST'])
@login_required # ¡Ruta protegida! Solo el usuario dueño del perfil puede editarlo.
def edit_profile():
    """
    Procesa el formulario de edición del perfil.
    Solo acepta peticiones POST.
    """
    # Gracias a Flask-Login, 'current_user' es el objeto Profile que debemos actualizar.
    profile_to_update = current_user

    # Obtenemos los nuevos datos del formulario que se envió.
    new_username = request.form.get('username')
    new_full_name = request.form.get('full_name')

    # Validamos que el nombre de usuario no esté vacío.
    if not new_username:
        flash('El nombre de usuario no puede estar vacío.', 'danger')
        return redirect(url_for('profile.view_profile'))

    # Actualizamos los campos del objeto de perfil en memoria.
    profile_to_update.username = new_username
    profile_to_update.full_name = new_full_name

    try:
        # Intentamos guardar los cambios en la base de datos.
        db.session.commit()
        flash('Tu perfil ha sido actualizado correctamente.', 'success')
    except Exception as e:
        # En caso de error (ej. el nuevo username ya existe), revertimos los cambios.
        db.session.rollback()
        flash(f'Error al actualizar el perfil. Es posible que el nombre de usuario ya esté en uso.', 'danger')
    
    # Redirigimos al usuario de vuelta a su página de perfil.
    return redirect(url_for('profile.view_profile'))
