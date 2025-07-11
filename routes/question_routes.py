from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Question, Answer, Tag
from app import db
from flask_login import current_user, login_required # <-- Importamos las herramientas

questions_bp = Blueprint('questions', __name__)

@questions_bp.route('/questions/<int:question_id>')
def view_question(question_id):
    """ Muestra una pregunta específica con sus respuestas. """
    question = Question.query.get_or_404(question_id)
    return render_template('preguntas.html', question=question)

@questions_bp.route('/ask', methods=['GET', 'POST'])
@login_required # <-- 1. Ruta protegida. El usuario DEBE iniciar sesión.
def ask_question():
    """ Muestra el formulario para preguntar y procesa el envío. """
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        tag_ids = request.form.getlist('tags')

        if not title or not body:
            flash('El título y el cuerpo de la pregunta son obligatorios.', 'danger')
            return redirect(url_for('questions.ask_question'))
        
        # --- LÍNEA CORREGIDA ---
        # 2. Usamos el ID del usuario actual de la sesión, no uno fijo.
        new_question = Question(title=title, body=body, user_id=current_user.id)

        if tag_ids:
            tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
            new_question.tags.extend(tags)

        try:
            db.session.add(new_question)
            db.session.commit()
            flash('Tu pregunta ha sido publicada con éxito.', 'success')
            return redirect(url_for('questions.view_question', question_id=new_question.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Ocurrió un error al publicar tu pregunta: {e}', 'danger')

    all_tags = Tag.query.order_by(Tag.name).all()
    return render_template('preguntar.html', tags=all_tags)
