from flask import Flask, render_template, session, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

from forms import CreateUserForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback-users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'SECRET'

debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def home_page():
    """ Redirects to register form """

    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def show_user_form():
    """ Show form to create a user """

    form = CreateUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()

        # TODO: add user id to session

        return redirect('/secret')
    
    else:
        return render_template('user_form.html', form=form)