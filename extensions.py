from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Aquí creamos las instancias de las extensiones, pero sin asociarlas a ninguna app todavía.
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
