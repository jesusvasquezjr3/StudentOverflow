from flask import Blueprint, request, render_template, redirect, url_for, flash
from app import supabase, db
from models import Profile
from flask_login import login_user, logout_user, login_required, current_user

# Creamos el Blueprint para las rutas de autenticación
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Maneja el inicio de sesión del usuario.
    Muestra el formulario en GET y procesa las credenciales en POST.
    """
    # Si el usuario ya está autenticado, redirigirlo a la página principal
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Se requieren tanto el email como la contraseña.', 'danger')
            return render_template('login.html')

        try:
            # 1. Autenticar las credenciales con el cliente de Supabase
            res = supabase.auth.sign_in_with_password({"email": email, "password": password})
            
            # 2. Si la autenticación es exitosa, buscar nuestro perfil local en la DB
            profile = Profile.query.filter_by(id=res.user.id).first()
            
            if profile:
                # 3. Usar Flask-Login para crear la sesión del usuario
                # El segundo argumento 'remember=True' crea una cookie persistente
                login_user(profile, remember=True)
                flash('¡Has iniciado sesión correctamente!', 'success')
                
                # Redirigir al usuario a la página a la que intentaba acceder, o a la principal
                next_page = request.args.get('next')
                return redirect(next_page or url_for('main.index'))
            else:
                # Esto es un caso raro: el usuario existe en Supabase Auth pero no en nuestra tabla de perfiles.
                flash('No se encontró un perfil de usuario asociado.', 'danger')

        except Exception as e:
            # El cliente de Supabase lanza una excepción si las credenciales son incorrectas
            flash('Email o contraseña incorrectos. Por favor, inténtalo de nuevo.', 'danger')
            
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Maneja el registro de un nuevo usuario.
    Muestra el formulario en GET y crea la cuenta en POST.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')

        if not email or not password or not username:
            flash('Todos los campos son obligatorios.', 'danger')
            return render_template('registro.html')

        try:
            # 1. Registrar el usuario en el sistema de autenticación de Supabase
            res = supabase.auth.sign_up({"email": email, "password": password})
            
            # 2. Si el registro en Supabase es exitoso, crear el perfil en nuestra tabla 'profiles'
            # Es crucial vincularlo con el mismo ID de usuario.
            new_profile = Profile(id=res.user.id, username=username)
            db.session.add(new_profile)
            db.session.commit()

            flash('¡Registro exitoso! Revisa tu correo electrónico para verificar tu cuenta.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            # Capturar posibles errores de la API de Supabase (ej: usuario ya existe)
            flash(f'Error en el registro: {e}', 'danger')
            
    return render_template('registro.html')

@auth_bp.route('/logout')
@login_required # Solo usuarios autenticados pueden acceder a esta ruta
def logout():
    """ Cierra la sesión del usuario actual. """
    logout_user() # Esta función de Flask-Login elimina la sesión del usuario
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('main.index'))
