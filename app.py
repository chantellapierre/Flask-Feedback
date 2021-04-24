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
    return redirect("/register")


###User routes

@app.route('/users/<username>', methods= ['GET', 'POST'])
def show_user_details(username):
    if "username" not in session:
        raise Unauthorized()
        flash("Please log in first!")
        user = User.query.get(username)
        form = DeleteForm
        return redirect('/login')
    return render_template('users/show.html', user=user, form=form)

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
        return redirect('/users/{user.username}')

    return render_template('users/register.html', form=form)


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
def delete_user(username):
    
    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return render_template('/login')

###Feedback routes

@app.route('/users/<username>/feedback/new', methods = ['GET', 'POST'])
def add_feedback():
    
    if "username" not in session:
        flash("Please log in first!", "danger")
        raise Unauthorized()
        return redirect('/login')

    form = FeedbackForm()

    feedback = Feedback.query.all()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
        title=title,
        content=content,
        username=username,
        )

        db.session.add(feedback)
        db.session.commit()

        flash("Feedback created!", "success")
        return redirect(f'/users/{feedback.username')

    else:
        return render_template('feedback.html', form=form)


@app.route('/feedback/<int:feedback_id>/update', methods = ['GET', 'POST'])
def update_feedback(feedback_id):
    
    feedback = Feedback.query.get(feedback_id)
    form = FeedbackForm()

    if 'username' not in session:
        raise Unauthorized()

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f'users/{feedback.username}')

    return render_template('feedback/edit.html', form=form, feedback=feedback)



@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    if 'username' not in session:
        flash("Please log in first!", "danger")
        raise Unauthorized()
        return redirect('/login')

    feedback = Feedback.query.get_or_404(id)

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")



