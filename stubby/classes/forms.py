class AddClass(FlaskForm):
    course = StringField('Course or CRN', validators=[DataRequired()])
    submit = SubmitField('Add Class')
