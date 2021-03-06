from flask import Flask, request, render_template, session, redirect, url_for, flash
from db import db
from models import User, Post
from helpers import pretty_date, login_required


def create_app():
    ''' To create the application object, and initialize all the extensions
    and configurations
    '''
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # register the pretty_date filter
    app.jinja_env.filters['pretty_date'] = pretty_date
    return app

app = create_app() # Create the application
# Binding the database connection to the application
db.init_app(app)
db.app = app

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # This is executed when the user submits the form.
        username = request.form['username']
        password = request.form['password']

        status, message = User.authenticate(username, password)

        if status:
            # Setup the session variables
            session['user_name'] = message['name']
            session['logged_in'] = True
            session['user_id'] = message['user_id']
            flash("Hello %s, %s" % (message['name'], message['message']), 'success')
            return redirect(url_for('index'))
        else:
            flash(message['message'], 'error')
            return redirect(url_for('login'))

    else:
        # This is executed when the user visits the above route.
        return render_template('login.html')

@app.route("/logout")
def logout():
    # Destroy the session variables
    session.pop('user_name', None)
    session.pop('logged_in', None)
    session.pop('user_id', None)
    flash('You have been logged out successful', 'success')
    return redirect(url_for('index'))

@app.route("/posts/create", methods=['POST'])
@login_required
def create_post():
    # Create a post
    body = request.form['body']
    p = Post(body=body, user_id=session['user_id'])
    if p.save():
        flash("Your post was created successfully.", "success")
    else:
        flash("There was a problem creating your post", "error")
    return redirect(url_for('show_posts'))

@app.route("/posts/", defaults={'user': None, 'page': 1}) # This allows me to use /posts/
@app.route("/posts/<user>/", defaults={'page': 1}) # Sets the default page to 1
@app.route("/posts/<int:page>", defaults={'user': None}) # Sets the default user to None
@app.route("/posts/<user>/<int:page>") # This allows me to see for a particular user.
@login_required
def show_posts(user, page):
    ''' Takes the "optional" username of the user and a page number to return the
    posts for the user '''
    RESULTS_PER_PAGE = 25
    OFFSET = max(0, (page - 1) * RESULTS_PER_PAGE)
    if user is None:
        posts = Post.query.order_by(Post.created.desc())\
                    .offset(OFFSET)\
                    .limit(RESULTS_PER_PAGE).all()
    else:
        user = User.query.filter_by(username=user).first()
        posts = Post.query.filter_by(user_id=user.id)\
                    .order_by(Post.created.desc())\
                    .offset(OFFSET)\
                    .limit(RESULTS_PER_PAGE).all()

    values = {
        "page": page, # So that we can give a link to the next page
        "posts": posts, # The list of all the posts
        "user": user, # Also, to generate the link
    }

    return render_template('show_posts.html', **values)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
