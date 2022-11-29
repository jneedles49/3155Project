# FLASK Tutorial 1 -- We show the bare-bones code to get an app up and running

# imports
import os

from flask import render_template, request, redirect, url_for, Flask

from database import db
from modelsProject import Project as Project
import bcrypt
from modelsProject import User as User
from flask import session
from modelsProject import Comment as Comment
from formsProject import RegisterForm, LoginForm, CommentForm

app = Flask(__name__)  # create an app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Bind SQLAlchemy db object to this flask app
db.init_app(app)

# Setup Models
with app.app_context():
    db.create_all()  # run under the app context


# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
@app.route('/')
@app.route('/indexProject')
def indexProject():
    if session.get('user'):
        return render_template("indexProject.html", user=session['user'])
    return render_template("indexProject.html")


@app.route('/projects')
def getProjects():
    a_user = db.session.query(User).filter_by(email='omikombo@uncc.edu').one()
    my_projects = db.session.query(Project).all()
    print(my_projects)
    return render_template('projects.html', projects=my_projects, user=a_user)


@app.route('/project/<project_id>')
def getProject(project_id):
    a_user = db.session.query(User).filter_by(email='omikombo@uncc.edu').one()
    my_project = db.session.query(Project).filter_by(id=project_id).one()
    return render_template('project.html', project=my_project, user=a_user)


@app.route('/projects/new', methods=['GET', 'POST'])
def newProject():
    a_user = {'name': 'Obed', 'email': 'omikombo@uncc.edu'}

    print('request method is', request.method)
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['projectText']
        from datetime import date
        today = date.today()
        today = today.strftime("%m-%d-%Y")
        new_record = Project(title, text, today)
        db.session.add(new_record)
        db.session.commit()

        return redirect(url_for('new_project'))
    else:
        a_user = db.session.query(User).filter_by(email='omikombo@uncc.edu').one()
        return render_template('newProject.html', user=a_user)


@app.route('/projects/edit/<project_id>', methods=['GET', 'POST'])
def editProject(project_id):
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['projectText']
        project = db.session.query(Project).filter_by(id=project_id).one()
        project.title = title
        project.text = text
        db.session.add(project)
        db.session.commit()

        return redirect(url_for('getProject'))
    else:
        a_user = db.session.query(User).filter_by(email='omikombo@uncc.edu').one()
        my_project = db.session.query(Project).filter_by(id=project_id).one()
        return render_template('newProject.html', project=my_project, user=a_user)


@app.route('/projects/delete/<project_id>', methods=['POST'])
def deleteProject(project_id):
    my_project = db.session.query(Project).filter_by(id=project_id).one()
    db.session.delete(my_project)
    db.session.commit()

    return redirect(url_for('getProject'))


@app.route('/registerProject', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        # salt and hash password
        h_password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        # get entered user data
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        # create user model
        new_user = User(first_name, last_name, request.form['email'], h_password)
        # add user to database and commit
        db.session.add(new_user)
        db.session.commit()
        # save the user's name to the session
        session['user'] = first_name
        session['user_id'] = new_user.id  # access id value from user model of this newly added user
        # show user dashboard view
        return redirect(url_for('getProjects'))

    # something went wrong - display register view
    return render_template('registerProject.html', form=form)


@app.route('/loginProject', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    # validate_on_submit only validates using POST
    if login_form.validate_on_submit():
        # we know user exists. We can use one()
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        # user exists check password entered matches stored password
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            # password match add user info to session
            session['user'] = the_user.first_name
            session['user_id'] = the_user.id
            # render view
            return redirect(url_for('getProjects'))

        # password check failed
        # set error message to alert user
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("loginProject.html", form=login_form)
    else:
        # form did not validate or GET request
        return render_template("loginProject.html", form=login_form)


@app.route('/logout')
def logout():
    # check if a user is saved in session
    if session.get('user'):
        session.clear()

    return redirect(url_for('indexProject'))


@app.route('/projects/<project_id>/comment', methods=['POST'])
def new_comment(project_id):
    if session.get('user'):
        comment_form = CommentForm()
        # validate_on_submit only validates using POST
        if comment_form.validate_on_submit():
            # get comment data
            comment_text = request.form['comment']
            new_record = Comment(comment_text, int(project_id), session['user_id'])
            db.session.add(new_record)
            db.session.commit()

        return redirect(url_for('get_project', note_id=project_id))

    else:
        return redirect(url_for('login'))


app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# project that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.
