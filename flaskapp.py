from flask import Flask, render_template, flash, request
from flask_bootstrap import Bootstrap
from flask_wtf import Form, RecaptchaField
from flask_wtf.file import FileField
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, IntegerField, FormField, validators


class SimpleForm(Form):
    fileName = FileField('Input file')

    submit_button = SubmitField('Run Code')

    def validate_hidden_field(form, field):
        raise ValidationError('Always wrong')


def solution(n, x, y):
    initial = x
    if x < 1:
        initial = 1
    result = []
    while initial < n:
        if (initial % x == 0) and (initial % y != 0):
            result.append(initial)
        initial += 1

    return result


app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = 'devkey'
app.config['RECAPTCHA_PUBLIC_KEY'] = \
    '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'


@app.route('/', methods=('GET', 'POST'))
def index():
    form = SimpleForm()
    if form.validate_on_submit():  # to get error messages to the browser
        values = request.files['fileName'].readlines()

        elems = int(values[0])
        if elems < 100:
            for value in values[1:]:
                n, x, y = value.split(' ')
                str_result = ' '.join(str(x) for x in solution(int(n), int(x), int(y)))
                flash(str_result)

    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run()