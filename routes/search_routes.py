from flask import Blueprint, render_template, request
from models import Question
from sqlalchemy import or_

search_bp = Blueprint('search', __name__)

@search_bp.route('/search')
def search():
    """
    Procesa la consulta de búsqueda del usuario y muestra los resultados.
    """
    # Obtener el término de búsqueda de los parámetros de la URL (?q=...)
    query = request.args.get('q', '')
    
    # Si la consulta no está vacía, buscar en la base de datos
    if query:
        # Usamos 'ilike' para una búsqueda case-insensitive (ignora mayúsculas/minúsculas)
        # y buscamos en el título y en el cuerpo de la pregunta.
        search_term = f"%{query}%"
        results = Question.query.filter(
            or_(
                Question.title.ilike(search_term),
                Question.body.ilike(search_term)
            )
        ).order_by(Question.created_at.desc()).all()
    else:
        # Si no hay término de búsqueda, no devolvemos resultados
        results = []

    return render_template('search.html', query=query, results=results)
