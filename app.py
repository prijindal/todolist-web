from flask import (Flask, render_template,send_from_directory,
                   flash, redirect, url_for, abort, request)

app = Flask(__name__)
app.secret_key = 'ech38iy3hci83gc3bic7gbc3b8igcb3nyuk'

import forms
import models


# GENERAL ROUTES
@app.route('/')
def index():
	return render_template("view.html",projects = models.Project.select().limit(100))

@app.route('/new', methods=['GET','POST'])
def new():
	form = forms.ProjectForm()
	if form.validate_on_submit():
		flash("Project Created!!")
		models.Project.create_project(
			name = form.name.data.strip(),
			description = form.description.data.strip()
		)
		return redirect(url_for('index'))
	return render_template('new.html', form=form)



# PROJECT ROUTES
@app.route('/<project>', methods=['GET'])
def project(project):
	try:
		project = models.Project.select().where(models.Project.url**project).get()
	except models.DoesNotExist:
		abort(404)
	else:
		stream = project.task.limit(100)
	return render_template('all.html', project=project, tasks = stream)

@app.route('/<project>/recent', methods=['GET'])
def project_recent(project):
	try:
		project = models.Project.select().where(models.Project.url**project).get()
	except models.DoesNotExist:
		abort(404)
	else:
		stream = project.task.where(models.Task.date_created==models.datetime.datetime.now()).limit(100) # Change this
	return render_template('all.html', project=project, tasks = stream)

@app.route('/<project>/completed', methods=['GET'])
def project_completed(project):
	try:
		project = models.Project.select().where(models.Project.url**project).get()
	except models.DoesNotExist:
		abort(404)
	else:
		stream = project.task.where(models.Task.completed == True).limit(100) # Change this
	return render_template('all.html', project=project, tasks = stream)

@app.route('/<project>/remaining', methods=['GET'])
def project_remaining(project):
	try:
		project = models.Project.select().where(models.Project.url**project).get()
	except models.DoesNotExist:
		abort(404)
	else:
		stream = project.task.where(models.Task.completed == False).limit(100) # Change this
	return render_template('all.html', project=project, tasks = stream)


@app.route("/<project>/delete", methods=['DELETE'])
def delete_project(project):
	if models.Project.delete().where(models.Project.url**project).execute():
		flash("Project Deleted!!")
		return "Succesful"
	else:
		flash("Project Not Found!!")
		return "not Succesful"

@app.route('/<project>/edit', methods=['POST'])
def project_edit(project):
	try:
		editDetails = dict(request.form.items())
		cur_project = models.Project.get(models.Project.url**project)
		cur_project.description = editDetails['newContent']
		cur_project.save()
		flash("New Data was Saved")
	except ValueError:
		flash("ERROR")
	return "successfull"


# TASKS ROUTES
@app.route("/<project>/create", methods=['GET','POST'])
def create(project):
	form = forms.TaskForm()
	if form.validate_on_submit():
		flash("Task Created!!")
		models.Task.create_task(
			title = form.title.data.strip(),
			details = form.details.data.strip(),
			lastdate = form.lastdate.data,
			project = models.Project.select().where(models.Project.url**project).get()
		)
		return redirect(url_for('project', project=project))
	return render_template('create.html', form=form)

@app.route("/<project>/<task>/delete", methods=['DELETE'])
def taskdelete(project, task):
	cur_project = models.Project.select().where(models.Project.url**project).get()
	if models.Task.delete().where(models.Task.url**task, cur_project.url==project).execute():
		flash("Task Deleted in {} Project!!".format(project))
		return "Succesful"
	else:
		flash("Task Not Found!!")
		return "not Succesful"

@app.route("/<project>/<task>/complete", methods=['PUT'])
def taskcomplete(project, task):
	return toggle_state(project, task, True)

@app.route("/<project>/<task>/remain", methods=['PUT'])
def taskremain(project, task):
	return toggle_state(project, task, False)

def toggle_state(project, task, newState):
	cur_project = models.Project.select().where(models.Project.url**project).get()
	try:
		cur_task = models.Task.get(models.Task.url**task, cur_project.url==project).get()
		cur_task.completed = newState
		cur_task.save()
		flash("Task was {}".format('done' if newState else 'undone'))
		return "Succesful"
	except ValueError:
		flash("Task Not Found!!")
		return "not Succesful"

@app.route("/<project>/<task>/edit", methods = ['POST'])
def task_edit(project, task):
	editDetails = dict(request.form.items())
	cur_project = models.Project.get(models.Project.url**project)
	try:
		cur_task = models.Task.get(models.Task.url**task, cur_project.url==project).get()
		cur_task.details = editDetails['newContent']
		cur_task.lastdate = editDetails['newDate']
		cur_task.save()
		flash("New Task Data was Saved")
		return "Succesful"
	except ValueError:
		flash("ERROR")
		return "unsuccesfull"




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




DEBUG = True
HOST = '0.0.0.0'
PORT = 8000

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)
