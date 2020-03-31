from flask import Flask, render_template, session, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback

from forms import CreateUserForm, LoginUserForm, FeedbackForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback-users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'SECRET'

debug = DebugToolbarExtension(app)

connect_db(app)
# db.drop_all()
db.create_all()


@app.route('/')
def home_page():
    """ Redirects to register form """

    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def show_user_form():
    """ Show form to create a user """
    if session.get('username'):
        return redirect(f"/users/{session.get('username')}")

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

        session['username'] = new_user.username

        return redirect(f"/users/{username}")

    else:
        return render_template('user_form.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def show_login_form():
    """ Show form to login a user """

    if session.get('username'):
        return redirect(f"/users/{session.get('username')}")

    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            return redirect('/secret')
        else:
            form.username.errors = ['Invalid login']

    return render_template('login.html', form=form)

@app.route("/users/<username>")
def display_user(username):
    if not session.get('username'):
        return redirect('/register')

    user = User.query.get_or_404(username)
    return render_template('user_page.html', user=user, session_username=session.get('username'))

@app.route("/users/<username>/feedback/add", methods=['GET', 'POST'])
def add_feedback(username):
    if session.get('username') != username:
        return redirect('/register')

    form = FeedbackForm()
    form.username.choices = (db.session.query(User.username, User.username).filter(User.username != username).all())

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        username = form.username.data
        feedback = Feedback(title=title, content=content, username=username)
        db.session.add(feedback)
        db.session.commit()
        return redirect(f"/users/{username}")

    else:
        return render_template('feedback_form.html', form=form)


@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    if session.get('username') == username:
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        session.pop("username")
    return redirect('/register')

@app.route('/secret')
def show_secret():
    """
    Shhh ;)
    """

    if session.get('username'):
        return render_template('secret.html')
    return redirect('/register')

@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    session.pop("username")

    return redirect('/register')

