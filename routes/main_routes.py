from flask import Blueprint, render_template
from models import Question

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Obtener las preguntas más recientes para mostrar en la página de inicio
    recent_questions = Question.query.order_by(Question.created_at.desc()).limit(10).all()
    return render_template('index.html', questions=recent_questions)
