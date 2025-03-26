# models.py
from . import db

class Questionnaire(db.Model):
    __tablename__ = 'questionnaire'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    questions = db.relationship('Question', backref='questionnaire', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Questionnaire ({self.id}) {self.name}>'

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'questions': [q.to_json() for q in self.questions]
        }

    @staticmethod
    def from_json(json_data):
        return Questionnaire(name=json_data['name'])

    def modify(self, json_data):
        self.name = json_data.get('name', self.name)
        return self

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    type = db.Column(db.String(50))
    answer = db.Column(db.String(256))
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id'))

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'base'
    }

    def __repr__(self):
        return f'<Question ({self.id}) {self.title}>'

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'type': self.type,
            'answer': self.answer,
            'questionnaire_id': self.questionnaire_id
        }

    @staticmethod
    def from_json(json_data):
        q_type = json_data.get('type')
        if q_type == 'open':
            return OpenQuestion.from_json(json_data)
        elif q_type == 'multiple_choice':
            return MultipleChoiceQuestion.from_json(json_data)
        else:
            raise ValueError("Type de question non reconnu.")

    def modify(self, json_data):
        self.title = json_data.get('title', self.title)
        self.answer = json_data.get('answer', self.answer)
        return self

class OpenQuestion(Question):
    __mapper_args__ = {
        'polymorphic_identity': 'open'
    }

    def to_json(self):
        base = super().to_json()
        return base

    @staticmethod
    def from_json(json_data):
        obj = OpenQuestion()
        obj.title = json_data.get('title', "")
        obj.type = 'open'
        obj.answer = json_data.get('answer', "")
        obj.questionnaire_id = json_data['questionnaire_id']
        return obj

class MultipleChoiceQuestion(Question):
    __mapper_args__ = {
        'polymorphic_identity': 'multiple_choice'
    }

    def to_json(self):
        base = super().to_json()
        return base

    @staticmethod
    def from_json(json_data):
        obj = MultipleChoiceQuestion()
        obj.title = json_data.get('title', "")
        obj.type = 'multiple_choice'
        obj.answer = json_data.get('answer', "")
        obj.questionnaire_id = json_data['questionnaire_id']
        return obj
