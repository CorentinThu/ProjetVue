from flask import Blueprint, render_template
bp_quiz_page = Blueprint('bp_quiz_page', __name__)

@bp_quiz_page.route("/")
def show_quiz():
    return render_template("quiz.html")
