from flask import Blueprint, render_template
from models import Tag, Question

tags_bp = Blueprint('tags', __name__)

@tags_bp.route('/tags')
def all_tags():
    """
    Muestra una lista de todas las etiquetas disponibles.
    Por defecto, no se selecciona ninguna etiqueta y no se muestran preguntas.
    """
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('etiquetas.html', tags=tags, selected_tag=None, questions=[])

@tags_bp.route('/tags/<string:tag_name>')
def questions_by_tag(tag_name):
    """
    Muestra todas las preguntas asociadas a una etiqueta específica.
    """
    # Encuentra la etiqueta en la base de datos
    tag = Tag.query.filter_by(name=tag_name).first_or_404()
    
    # Obtiene todas las etiquetas para la barra lateral
    all_tags_list = Tag.query.order_by(Tag.name).all()
    
    # Las preguntas se obtienen de la relación definida en el modelo
    questions_for_tag = tag.questions.order_by(Question.created_at.desc()).all()
    
    return render_template(
        'etiquetas.html', 
        tags=all_tags_list, 
        selected_tag=tag, 
        questions=questions_for_tag
    )
