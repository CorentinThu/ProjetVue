# routes/question_routes.py
from flask import Blueprint, request, jsonify, abort
from .. import db
from ..flakk.models import Question, Questionnaire

bp_question = Blueprint('bp_question', __name__)

@bp_question.route('/questions', methods=['POST'])
def create_question():
    """
    data = {
      "title": "...",
      "type": "open" ou "multiple_choice",
      "questionnaire_id": <id du questionnaire>,
      "answer": "Réponse facultative"
    }
    """
    data = request.get_json()
    if not data:
        abort(400, description="Données invalides.")

    questionnaire_id = data.get('questionnaire_id')
    if not questionnaire_id:
        abort(400, description="L'ID du questionnaire est obligatoire.")

    questionnaire = Questionnaire.query.get(questionnaire_id)
    if not questionnaire:
        abort(400, description="Le questionnaire spécifié n'existe pas.")

    try:
        new_question = Question.from_json(data)
    except ValueError as e:
        abort(400, description=str(e))

    db.session.add(new_question)
    db.session.commit()
    return jsonify(new_question.to_json()), 201

@bp_question.route('/questions/<int:q_id>', methods=['GET'])
def get_question(q_id):
    question = Question.query.get_or_404(q_id)
    return jsonify(question.to_json())

@bp_question.route('/questions/<int:q_id>', methods=['PUT'])
def update_question(q_id):
    question = Question.query.get_or_404(q_id)
    data = request.get_json()
    question.modify(data)
    db.session.commit()
    return jsonify(question.to_json())

@bp_question.route('/questions/<int:q_id>', methods=['DELETE'])
def delete_question(q_id):
    question = Question.query.get_or_404(q_id)
    db.session.delete(question)
    db.session.commit()
    return jsonify({'result': True})