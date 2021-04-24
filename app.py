from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import UserForm, LoginForm, LogoutForm, FeedbackForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flask_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "ihaveasecret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    return render_template('index.html')


###User routes

@app.route('/users/<username>', methods= ['GET', 'POST'])
def show_user_details(username):
    if "username" not in session:
        raise Unauthorized()
        flash("Please log in first!")
        user = User.query.get(username)
        form = DeleteForm
        return redirect('/login')
    return render_template('details.html', user=user, form=form)

@app.route('/register', methods = ['GET', 'POST'])
def register_user():

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password)

        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        flash('Welcome! Successfully created new account.')
        return redirect('/users/<username>')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()
    
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome back, {user.first_name}!")
            session['user_id'] = user.id
            return redirect('/users/{user.username}')
        else:
            form.username.errors = ["Invalid login information"]

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_user():
    session.pop('user_id')
    flash("Goodbye!")
    return redirect('/login')

@app.route('/users/<username>/delete')
def delete_user():
    return render_template('/')

###Feedback routes

@app.route('/users/<username>/feedback/add', methods = ['GET', 'POST'])
def add_feedback():
    if "user_id" not in session:
        flash("Please log in first!", "danger")
        return redirect('/login')
    form = FeedbackForm()
    feedback = Feedback.query.all()
    if form.validate_on_submit():
        text = form.text.data
        new_feedback = Feedback(text=text, user_id = session["user_id"])

        db.session.add(new_feedback)
        db.session.commit()
        flash("Feedback created!", "success")
        redirect('/feedback')
    return render_template('feedback.html', form=form, Feedback=feedback)

@app.route('/feedback/<int:id>/update', methods = ['GET'])
def update_feedback_form():
    form = FeedbackForm()
    return render_template('feedback.html', form=form)

@app.route('/feedback/<int:id>/update', methods = ['POST'])
def post_update_feedback():
    return render_template('feedback.html')

@app.route('/feedback/<int:id>/delete', methods=['POST'])
def delete_feedback(id):
    if 'user_id' not in session:
        flash("Please log in first!", "danger")
        return redirect('/login')
    feedback = Feedback.query.get_or_404(id)
    if feedback.user_id == session['user_id']:
        db.session.delete(feedback)
        db.session.commit()
        flash("Feedback deleted", "success")
        return redirect('/feedback')
    flash("You don't have permission to do that!")
    return redirect('/feedback')



