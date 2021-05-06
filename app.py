from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import surveys
from random import choice


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hush'
debug = DebugToolbarExtension(app)

current_survey = surveys.surveys["satisfaction"]


@app.route('/')
def home():
    return render_template("home.html", survey=current_survey)


@app.route('/initialize', methods=['POST'])
def initialize():
    session['responses'] = []
    return redirect('/question/0')


@app.route('/question/<int:num>')
def question(num):
    answered = len(session['responses'])
    if answered == len(current_survey.questions):
        return redirect('/thanks')
    elif num != answered:
        flash("Sorry, you are trying to access an invalid question.")
        return redirect('/question/' + str(answered))

    curr_question = current_survey.questions[num]
    return render_template("question.html", question=curr_question, title=current_survey.title, num=num)


@app.route('/answer', methods=['POST'])
def answer():
    responses = session['responses']
    responses.append(request.form["choice"])
    session['responses'] = responses
    num = request.args.get('num')
    if int(num) < len(current_survey.questions):
        return redirect('/question/'+num)
    else:
        return redirect('/thanks')


@app.route('/thanks')
def thanks():
    return render_template('thanks.html')
