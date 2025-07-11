from flask import Blueprint, request, redirect, url_for, flash
from app import db
from models import Answer, Question
# from flask_login import current_user, login_required

answer_bp = Blueprint('answers', __name__)

@answer_bp.route('/questions/<int:question_id>/answer', methods=['POST'])
# @login_required
def post_answer(question_id):
    """ Procesa el envío del formulario para una nueva respuesta. """
    body = request.form.get('body')

    if not body:
        flash('La respuesta no puede estar vacía.', 'danger')
        return redirect(url_for('questions.view_question', question_id=question_id))

    # Verificar que la pregunta exista
    question = Question.query.get_or_404(question_id)

    # En un sistema real, el ID del usuario vendría de la sesión
    # user_id_actual = current_user.id
    user_id_actual = "a4b6c3d9-93d5-4e3a-8f7b-2d7c8e9f0a1b" # Usando el ID de Ana Pérez para pruebas

    new_answer = Answer(
        body=body,
        question_id=question.id,
        user_id=user_id_actual
    )

    try:
        db.session.add(new_answer)
        db.session.commit()
        flash('Tu respuesta ha sido publicada.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al publicar la respuesta: {e}', 'danger')

    return redirect(url_for('questions.view_question', question_id=question_id))
