from flask import Blueprint, request, redirect, url_for, flash
from app import db
from models import Answer, Question
from flask_login import current_user, login_required # <-- Importamos las herramientas

answer_bp = Blueprint('answers', __name__)

@answer_bp.route('/questions/<int:question_id>/answer', methods=['POST'])
@login_required # <-- 1. Ruta protegida.
def post_answer(question_id):
    """ Procesa el envío del formulario para una nueva respuesta. """
    body = request.form.get('body')

    if not body:
        flash('La respuesta no puede estar vacía.', 'danger')
        return redirect(url_for('questions.view_question', question_id=question_id))

    question = Question.query.get_or_404(question_id)

    # --- LÍNEA CORREGIDA ---
    # 2. Usamos el ID del usuario de la sesión.
    new_answer = Answer(
        body=body,
        question_id=question.id,
        user_id=current_user.id
    )

    try:
        db.session.add(new_answer)
        db.session.commit()
        flash('Tu respuesta ha sido publicada.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al publicar la respuesta: {e}', 'danger')

    return redirect(url_for('questions.view_question', question_id=question_id))
