import os

class Config:
    """
    Configuración para la aplicación Flask.
    Carga la URI de la base de datos desde las variables de entorno para mayor seguridad.
    """
    # --- IMPORTANTE ---
    # Reemplaza la siguiente línea con tu URI de conexión de Supabase.
    # Es una MEJOR PRÁCTICA guardarla como una variable de entorno y no directamente en el código.
    # Ejemplo: 'postgresql://postgres:[TU_CONTRASENA]@[ID_PROYECTO].db.supabase.co:5432/postgres'
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://user:password@host:port/database')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Clave secreta para sesiones y seguridad de formularios
    SECRET_KEY = os.environ.get('SECRET_KEY', 'una-clave-secreta-muy-segura-para-desarrollo')

    # Configuración de Supabase (reemplaza con tus propias claves)
    SUPABASE_URL = os.environ.get('SUPABASE_URL', 'URL_DE_TU_PROYECTO_SUPABASE')
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY', 'KEY_PUBLICA_DE_SUPABASE')
