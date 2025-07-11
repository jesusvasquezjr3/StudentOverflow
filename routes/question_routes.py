from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Question, Answer, Tag
from app import db
# from flask_login import current_user, login_required # Se usará en el futuro

questions_bp = Blueprint('questions', __name__)

@questions_bp.route('/questions/<int:question_id>')
def view_question(question_id):
    """ Muestra una pregunta específica con sus respuestas. """
    question = Question.query.get_or_404(question_id)
    return render_template('preguntas.html', question=question)

@questions_bp.route('/ask', methods=['GET', 'POST'])
# @login_required # Protegeremos esta ruta en el futuro
def ask_question():
    """ Muestra el formulario para preguntar y procesa el envío. """
    if request.method == 'POST':
        # --- Lógica de envío del formulario ---
        title = request.form.get('title')
        body = request.form.get('body')
        tag_ids = request.form.getlist('tags') # getlist para múltiples selecciones

        if not title or not body:
            flash('El título y el cuerpo de la pregunta son obligatorios.', 'danger')
            return redirect(url_for('questions.ask_question'))
        
        # En un sistema real, obtendríamos el ID del usuario de la sesión
        # user_id_actual = current_user.id 
        user_id_actual = "a4b6c3d9-93d5-4e3a-8f7b-2d7c8e9f0a1b" # ID de Ana Pérez para pruebas

        # Crear la nueva pregunta
        new_question = Question(title=title, body=body, user_id=user_id_actual)

        # Asociar las etiquetas seleccionadas
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

    # --- Lógica para mostrar el formulario ---
    # Cargar todas las etiquetas para mostrarlas en el dropdown
    all_tags = Tag.query.order_by(Tag.name).all()
    return render_template('preguntar.html', tags=all_tags)
