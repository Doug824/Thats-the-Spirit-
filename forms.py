from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length

class RegisterForm(FlaskForm):
    """Form for adding users."""
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])

class LoginForm(FlaskForm):
    """Login form."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class RecommendForm(FlaskForm):
    """Recommendation form"""
    username = StringField('User Name', render_kw={"disabled":True}, validators=[DataRequired()])
    recommend_to_name = SelectField('Recommend To', validators=[DataRequired()])
    drink = StringField('Drink Name', render_kw={"disabled":True}, validators=[DataRequired()])