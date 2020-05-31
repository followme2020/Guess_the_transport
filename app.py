
from flask import Flask, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms.fields import RadioField, StringField, SubmitField
from wtforms.validators import DataRequired
from guess import Guess, GuessError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
game = Guess('Motorcycle')
game.expand('Motorcycle', 'Car', 'It has 4 wheels?', True)
game.expand('Car', 'Truck', 'Can carry goods?', True)
game.expand('Truck', 'Train', 'It travel by rail?', True)





class YesNoQuestionForm(FlaskForm):
    answer = RadioField('Your answer', choices=[('yes', 'Yes'), ('no', 'No')])
    submit = SubmitField('Submit')


class LearnForm(FlaskForm):
    vehicle = StringField('What vehicle did you pick?',
                          validators=[DataRequired()])
    question = StringField('what is a question that differentiates your'
                           'vehicle from mine?', validators=[DataRequired()])
    answer = RadioField('What is the answer for your question?',
                        choices=[('yes', 'Yes'), ('no', 'No')])
    submit = SubmitField('Submit')


@app.route('/')
def index():
    session['question'] = 0
    return render_template('index.html')


@app.route('/question', methods=['GET', 'POST'])
def question():
    if 'question' not in session:
        # if there is no question in the session go to start page
        return redirect(url_for('index'))

    id = session['question']
    question = game.get_question(id)
    if question is None:
        # if there is no question, we are in the end of the game,
        # redirect to guess page
        return redirect(url_for('guess'))

    form = YesNoQuestionForm()
    if form.validate_on_submit():
        # user answered the question, advance to the next question
        session['question'] = game.answer_question(form.answer.data == 'yes', id)
        return redirect(url_for('question'))
        # present the question to the user
    return render_template('question.html', question=question, form=form)


@app.route('/guess', methods=['GET', 'POST'])
def guess():
    if 'question' not in session:
        # if there is no question in the session we go to start page
        return redirect(url_for('index'))
    id = session['question']
    guess = game.get_guess(id)
    if guess is None:
        # there is no guess, shoudnt be here
        return redirect(url_for('index'))
    form = YesNoQuestionForm()
    if form.validate_on_submit():
        if form.answer.data == 'yes':
            # a sucsesful guess was made, game over
            return redirect(url_for('index'))
        # ask the user to expand the game with a new question
        return redirect(url_for('learn'))
    # present the guess to user
    return render_template('guess.html', guess=guess, form=form)


@app.route('/learn', methods=['GET', 'POST'])
def learn():
    if 'question' not in session:
        # if there is no question in the session we go to start page
        return redirect(url_for('index'))

    id = session['question']
    guess = game.get_guess(id)
    if guess is None:
        # there is no guess, shoudnt be here
        return redirect(url_for('index'))

    form = LearnForm()
    if form.validate_on_submit():
        game.expand(guess, form.vehicle.data, form.question.data,
                    form.answer.data == 'yes')
        return redirect(url_for('index'))
    return render_template('learn.html', guess=guess, form=form)


@app.errorhandler(GuessError)
@app.errorhandler(404)
def runtime_error(e):
    return render_template('error.html', error=str(e))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)