
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms.fields import RadioField, SubmitField
from guess import Guess

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
game = Guess('Car')
game.expand('Car', 'Motor Cycle', 'It has 4 wheels?', False)
game.expand('Motor Cycle', 'Train', '2 wheels?', False)


class YesNoQuestionForm(FlaskForm):
    answer = RadioField('Your answer', choices=[('yes', 'Yes'), ('no', 'No')])
    submit = SubmitField('Submit')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/question/<int:id>', methods=['GET','POST'])
def question(id):
    question = game.get_question(id)
    if question is None:
        return redirect(url_for('guess', id=id))
    form = YesNoQuestionForm()
    if form.validate_on_submit():
        new_id = game.answer_question(form.answer.data == 'yes', id)
        return redirect(url_for('question', id=new_id))
    return render_template('question.html', question=question, form=form)

@app.route('/guess/<int:id>')
def guess(id):
    return render_template('guess.html', guess=game.get_guess(id))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)