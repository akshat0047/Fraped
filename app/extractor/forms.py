from flask_wtf import Form
from wtforms import SelectField, TextField, SubmitField


class ApiForm(Form):
    url = TextField("Enter URL")
    Extract = SelectField(
        'Extract',
        choices=[('lop', 'Links on a page'), ('lopd', 'Links on a Domain'),
                 ('sp', 'Headers on a Single Page'), ('dh',  'Headers On a domain')]
    )
    Depth = SelectField(
        'Depth',
        choices=[('1', '1'), ('2', '2'),
                 ('3', '3'), ('4',  '4'), ('5',  '5'), ('0',  '0 ')]
    )
    submit = SubmitField("Submit")
