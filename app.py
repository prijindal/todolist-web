import os
import datetime

from flask import (Flask,send_from_directory,
				   request, redirect, make_response,
				   url_for)
from flask import render_template
import database

app = Flask(__name__)


@app.route('/')
def index():
	return render_template("view.html",projects = database.get_projects())

@app.route('/new')
def new():
	return render_template("create_project.html")

@app.route('/save',methods=['POST'])
def save():
	projectInfo = dict(request.form.items())
	response = make_response(redirect(url_for(".index")))
	database.create_project(projectInfo["title"],projectInfo["description"])
	response.set_cookie('last_url',projectInfo['title'].replace(' ','_'))
	return response


@app.route("/<project>/delete")
def delete_project(project):
	database.delete_project(project)
	return "successfull"

@app.route('/<project>')
def all_tasks(project):
	projectdetails = database.project_details_all(project)
	response = make_response(render_template("all.html",**projectdetails))
	response.set_cookie('last_url',projectdetails['url'])
	return response

@app.route('/<project>/recent')
def recent_tasks(project):
	projectdetails = database.project_details_recent(project)

	return render_template("all.html",**projectdetails)

@app.route('/<project>/completed')
def completed_tasks(project):
	projectdetails = database.project_details_completed(project)

	return render_template("all.html",**projectdetails)

@app.route('/<project>/remaining')
def remaining_tasks(project):
	projectdetails = database.project_details_remaining(project)

	return render_template("all.html",**projectdetails)

@app.route('/<project>/edit', methods=['POST'])
def project_edit(project):
	editDetails = dict(request.form.items())
	database.editproject(project, editDetails['newContent'])
	return "successfull"

@app.route("/<project>/create")
def create_tasks(project):
	projectdetails = database.project_details(project)
	return render_template("create.html",**projectdetails)

@app.route("/<project>/save",methods=['POST'])
def save_tasks(project):
	taskInfo = dict(request.form.items())
	database.create_task(project,taskInfo)
	return redirect(url_for('all_tasks',project=project.replace(' ','_')))

@app.route("/<project>/<task>/delete")
def taskdelete(project, task):
	database.delete_task(project,task)
	return "successfull"


@app.route("/<project>/<task>/complete")
def taskcomplete(project, task):
	database.markcomplete(project,task)
	return "successfull"


@app.route("/<project>/<task>/remain")
def taskremain(project, task):
	database.markremain(project,task)
	return "successfull"


@app.route("/<project>/<task>/edit", methods = ['POST'])
def taskedit(project, task):
	data = dict(request.form.items())
	newContent = data['newContent']
	newDate = data['newDate']
	database.editTask(project, task, newContent, newDate)
	return "successfull"

def check_date(current):
	print(datetime.datetime.now, current)




@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/bower_components/<path:path>')
def send_bower(path):
    return send_from_directory('bower_components', path)

@app.route('/foundation-icons/<path:path>')
def send_icons(path):
    return send_from_directory('foundation-icons', path)

@app.route('/favicon.ico')
def send_favicon():
    return "none"

app.run(debug=True,port = int(os.environ.get('PORT', 5000)))
