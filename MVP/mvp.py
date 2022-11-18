# FLASK Tutorial 1 -- We show the bare-bones code to get an app up and running

# imports
import os

from flask import render_template, request, redirect, url_for, Flask

from databaseProject import db
from modelsProject import Project as Project

from modelsProject import User as User
from flask import session

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
@app.route('/index')
def index():
    if session.get('user'):
        return render_template("index.html", user=session['user'])
    return render_template("index.html")


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
        return render_template('new.html', user=a_user)


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
        return render_template('new.html', project=my_project, user=a_user)


@app.route('/projects/delete/<project_id>', methods=['POST'])
def deleteProject(project_id):
    my_project = db.session.query(Project).filter_by(id=project_id).one()
    db.session.delete(my_project)
    db.session.commit()

    return redirect(url_for('getProject'))


app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# project that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.
