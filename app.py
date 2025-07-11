from flask import Flask, g
from config import Config
from supabase import create_client, Client

# --- 1. Importar las instancias desde extensions.py ---
from extensions import db, migrate, login_manager

supabase: Client = None

def create_app():
    """
    Fábrica de aplicaciones para crear y configurar la instancia de Flask.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # --- 2. Inicializar las extensiones importadas con la app ---
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Configurar cliente de Supabase
    global supabase
    supabase = create_client(app.config['SUPABASE_URL'], app.config['SUPABASE_KEY'])

    with app.app_context():
        # Importar modelos después de inicializar db
        from models import Profile
        from flask_login import current_user

        @login_manager.user_loader
        def load_user(user_id):
            return Profile.query.get(user_id)

        # --- SECCIÓN CORREGIDA Y CRUCIAL ---
        @app.before_request
        def before_request_func():
            """
            Esta función se ejecuta antes de cada petición.
            Asigna el usuario actual (autenticado o anónimo) al objeto global 'g'.
            """
            g.user = current_user
        # ------------------------------------

        # Registrar Blueprints
        from routes.main_routes import main_bp
        from routes.auth_routes import auth_bp
        from routes.question_routes import questions_bp
        from routes.answer_routes import answer_bp
        from routes.profile_routes import profile_bp
        from routes.search_routes import search_bp
        from routes.tags_routes import tags_bp
        from routes.user_routes import user_bp
        
        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(questions_bp)
        app.register_blueprint(answer_bp)
        app.register_blueprint(profile_bp)
        app.register_blueprint(search_bp)
        app.register_blueprint(tags_bp)
        app.register_blueprint(user_bp)


        # Crear tablas si no existen
        db.create_all()

    return app
