from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField

from wtforms.validators import InputRequired, Email, Length

class CreateUserForm(FlaskForm):
    """ Form for creating users """

    username = StringField("User Name",
                            validators=[InputRequired(),
                                        Length(1, 20)])

    password = PasswordField("Password",
                            validators=[InputRequired()])

    email = StringField("Email",
                            validators=[InputRequired(),
                                        Email(), Length(1, 50)])

    first_name = StringField("First Name",
                            validators=[InputRequired(),
                                        Length(1, 30)])

    last_name = StringField("Last Name",
                            validators=[InputRequired(),
                                        Length(1, 30)])

class LoginUserForm(FlaskForm):
    """ Form for logging in users """

    username = StringField("User Name",
                            validators=[InputRequired(),
                                        Length(1, 20)])

    password = PasswordField("Password",
                            validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    """ Form for adding feedback by a user """

    title = StringField("Title",
                            validators=[InputRequired(),
                                        Length(1, 100)])

    content = StringField("Content",
                            validators=[InputRequired()])

    username = SelectField("Feedback to",
                            validators=[InputRequired()])