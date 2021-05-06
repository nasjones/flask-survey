from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
import surveys
from random import choice


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hush'
debug = DebugToolbarExtension(app)
responses = []
current_survey = surveys.surveys["satisfaction"]


@app.route('/')
def home():
    return render_template("home.html", survey=current_survey)


@app.route('/question/<int:num>')
def question(num):
    if len(responses) == len(current_survey.questions):
        return redirect('/thanks')
    elif num != len(responses):
        flash("Sorry, you are trying to access an invalid question.")
        return redirect('/question/' + str(len(responses)))

    curr_question = current_survey.questions[num]
    return render_template("question.html", question=curr_question, title=current_survey.title, num=num)


@app.route('/answer', methods=['POST'])
def answer():
    responses.append(request.form["choice"])
    num = request.args.get('num')
    if int(num) < len(current_survey.questions):
        return redirect('/question/'+num)
    else:
        return redirect('/thanks')


@app.route('/thanks')
def thanks():
    return render_template('thanks.html')
