
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import Form
from wtforms.fields import RadioField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
questions = ['Does it sail?', 'It travels over rails?']
guesses = ['Car', 'Ship', 'Train']


class YesNoQuestionForm(Form):
    answer = RadioField('Your answer', choices=[('yes', 'Yes'), ('no', 'No')])
    submit = SubmitField('Submit')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/question/<int:id>', methods=['GET','POST'])
def question(id):
    form = YesNoQuestionForm()
    if form.validate_on_submit():
        if form.answer.data == 'yes':
            return redirect(url_for('question', id=id+1))
        else:
            return redirect(url_for('question', id=id))
    return render_template('question.html', question=questions[id], form=form)

@app.route('/guess/<int:id>')
def guess(id):
    return render_template('guess.html', guess=guesses[id])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)