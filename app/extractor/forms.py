from flask_wtf import Form
from wtforms import SelectField, TextField, IntegerField, SubmitField, validators


class ApiForm(Form):
    url = TextField("Enter URL")
    Extract = SelectField(
        'Extract',
        choices=[('sp', 'Headers on a Single Page'), ('dh',  'Headers On a domain'),
                 ('lop', 'Links on a page'), ('lopd', 'Links on a Domain')]
    )
    Depth = IntegerField('Depth', [validators.NumberRange(min=0, max=233)])

    submit = SubmitField("Submit")
