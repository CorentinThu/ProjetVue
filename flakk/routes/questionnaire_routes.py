# routes/questionnaire_routes.py
from flask import Blueprint, request, jsonify, abort
from .. import db
from ..flakk.models import Questionnaire

bp_questionnaire = Blueprint('bp_questionnaire', __name__)

@bp_questionnaire.route('/questionnaires', methods=['GET'])
def get_questionnaires():
    questionnaires = Questionnaire.query.all()
    return jsonify([q.to_json() for q in questionnaires])

@bp_questionnaire.route('/questionnaires/<int:q_id>', methods=['GET'])
def get_questionnaire(q_id):
    questionnaire = Questionnaire.query.get_or_404(q_id)
    return jsonify(questionnaire.to_json())

@bp_questionnaire.route('/questionnaires', methods=['POST'])
def create_questionnaire():
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, description="Nom du questionnaire manquant.")
    new_q = Questionnaire.from_json(data)
    db.session.add(new_q)
    db.session.commit()
    return jsonify(new_q.to_json()), 201

@bp_questionnaire.route('/questionnaires/<int:q_id>', methods=['PUT'])
def update_questionnaire(q_id):
    questionnaire = Questionnaire.query.get_or_404(q_id)
    data = request.get_json()
    questionnaire.modify(data)
    db.session.commit()
    return jsonify(questionnaire.to_json())

@bp_questionnaire.route('/questionnaires/<int:q_id>', methods=['DELETE'])
def delete_questionnaire(q_id):
    questionnaire = Questionnaire.query.get_or_404(q_id)
    db.session.delete(questionnaire)
    db.session.commit()
    return jsonify({'result': True})