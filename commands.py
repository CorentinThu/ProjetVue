import click
from flask.cli import with_appcontext
from .models import db, Questionnaire, OpenQuestion, MultipleChoiceQuestion

@click.command('syncdb')
@with_appcontext
def syncdb():
    """Crée et initialise la base de données."""
    db.drop_all()
    db.create_all()

    q1 = Questionnaire(name="Harry Potter")
    q2 = Questionnaire(name="Animaux")
    db.session.add(q1)
    db.session.add(q2)
    db.session.commit()

    question1 = OpenQuestion(title="Quel est le Patronus de Harry dans la saga du même nom ?", questionnaire_id=q1.id)
    question2 = MultipleChoiceQuestion(title="Quel est l'animal le plus mignon du monde ?", questionnaire_id=q2.id)
    db.session.add(question1)
    db.session.add(question2)
    db.session.commit()

    print("Base de données synchronisée avec succès !")
