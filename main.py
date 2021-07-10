from operator import mod
from flask import Flask, redirect, session, request, render_template, flash, url_for
from sqlalchemy.orm import Session
from datetime import date

from forms import AddProjectForm, EditProjectForm, SignUpForm, SignInForm, AddTaskForm, UD_Task_Form, EditTaskForm,SearchForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

basedir = os.path.abspath(os.path.dirname('__file__'))

app = Flask(__name__)
app.config['SECRET_KEY'] = '8192hdw8y31993r9128yw98y3yewe13'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

import models


@app.route('/')
def main():
    todolist = [
        {
            'name': 'Buy milk',
            'description': 'Buy 2 litter of milk in Coopmart.'
        },
        {
            'name': 'Get money',
            'description': 'Get 500k from ATM'
        }
    ]
    return render_template('index.html', todolist=todolist)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        _fname = form.inputFirstName.data
        _lname = form.inputLastName.data
        _email = form.inputEmail.data
        _password = form.inputPassword.data

        if db.session.query(models.User).filter_by(email=_email).count() == 0:
            user = models.User(first_name=_fname, last_name=_lname, email=_email)
            user.set_password(_password)
            db.session.add(user)
            db.session.commit()

            return render_template('signupSuccess.html', user=user)
        else:
            flash('Email {} is already exist!'.format(_email))
            return render_template('signup.html', form=form)

    return render_template('signup.html', form=form)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()

    if form.validate_on_submit():
        _email = form.inputEmail.data
        _password = form.inputPassword.data
        user = db.session.query(models.User).filter_by(email=_email).first()
        if user is None:
            flash('Wrong email or password!')
        else:
            if user.check_password(_password):
                session['user'] = user.user_id
                # session['taskDes']=""
                # return render_template('userhome.html',user=user)
                return redirect(url_for('userhome'))
            else:
                flash('Wrong  password!')

    return render_template('signin.html', form=form)




@app.route('/userhome', methods=['GET', 'POST'])
def userhome():
    form = AddProjectForm()
    _userId = session.get('user')
    searchForm = SearchForm()
    formx=UD_Task_Form()
    editProjectForm=EditProjectForm()
    searchForm.inputStatus.choices=[(0,"ALL"),(1,"running"),(3,"finished")]

    if _userId:
        user = db.session.query(models.User).filter_by(user_id=_userId).first()
        

        projectArray= db.session.query(models.Project).filter_by(user_id=_userId).all()


        if editProjectForm.submitEditProject.data and editProjectForm.validate_on_submit():
            project=db.session.query(models.Project).filter_by(project_id=session.get('project')).first()
            project.descripton=editProjectForm.inputProjectDescription.data
            project.name=editProjectForm.inputProjectName.data
            project.deadline=editProjectForm.inputProjectDeadline.data
            db.session.commit()

        if formx.validate_on_submit():
            for project in projectArray:
                if "update"+str(project.project_id) in request.form:
                    session['project']=project.project_id
                    return redirect(url_for('task'))                  
                elif "move_to_trash" + str(project.project_id) in request.form:                    
                    project.status_id
                    db.session.commit()                    
                elif "done" + str(project.project_id) in request.form:
                    session['project'] = project.project_id
                    return render_template('userhome.html', form=form, user=user,editProjectForm=editProjectForm, searchForm=searchForm,projectID=project.project_id)
                    
                


        if searchForm.submitSearch.data and searchForm.validate_on_submit():
            
            for project in projectArray:
                if (project.description.find(searchForm.inputSearchContent.data) != -1 or project.name.find(searchForm.inputSearchContent.data) != -1) and (project.status_id == searchForm.inputStatus.data or searchForm.inputStatus.data==0 ):    
                    session['content']=searchForm.inputSearchContent.data
                    session['table']="project"
                    session['status']=searchForm.inputStatus.data
                    return redirect(url_for('search'))
            flash("No result for '"+ searchForm.inputSearchContent.data +"'") 


        #if editTaskForm.submitEditTask.data and editTaskForm.validate():
        #    task = db.session.query(models.Task).filter_by(task_id=session.get('task')).first()
        #    task.description = editTaskForm.inputTaskDescription.data
        #    task.priority_id = editTaskForm.inputPriority.data
        #    db.session.commit()


        



        if form.submit.data and form.validate():
            project = models.Project(name=form.inputProjectName.data, description=form.inputProjectDescription.data, deadline=form.inputProjectDeadline.data, user_id=_userId, status_id=1)
            db.session.add(project)
            db.session.commit()
            return redirect(url_for('userhome'))
        return render_template('userhome.html', form=form, user=user,editProjectForm=editProjectForm , searchForm=searchForm, projectID=None)
    else:
        redirect('/')

@app.route('/completed', methods=['GET', 'POST'])
def completed():
    _userId = session.get('user')
    if _userId:
        user = db.session.query(models.User).filter_by(user_id=_userId).first()

        return render_template('completed.html', user=user)
    else:
        return redirect(url_for('userhome'))

@app.route('/trash', methods=['GET', 'POST'])
def trash():
    _userId = session.get('user')
    if _userId:
        user = db.session.query(models.User).filter_by(user_id=_userId).first()

        return render_template('trash.html', user=user)
    else:
        return redirect(url_for('userhome'))

@app.route('/task', methods=['GET', 'POST'])
def task():
    _projectID=session.get('project')
    form=AddTaskForm()
    editTaskForm=EditTaskForm()
    formx=UD_Task_Form()
    searchForm=SearchForm()
    taskArray= db.session.query(models.Task).filter_by(project_id=_projectID).all()
    
    

    if _projectID:
        project=db.session.query(models.Project).filter_by(project_id=_projectID).first()
        form.inputPriority.choices = [(p.priority_id, p.text) for p in db.session.query(models.Priority).all()]
        editTaskForm.inputPriority.choices = [(p.priority_id, p.text) for p in db.session.query(models.Priority).all()]        
        searchForm.inputStatus.choices=[(0,"ALL"),(1,"running"),(3,"finished")]
        

        if formx.validate_on_submit():
            for task in taskArray:
                if "update"+str(task.task_id) in request.form:
                    session['task'] = task.task_id
                    return render_template('task.html', form=form, project=project,editTaskForm=editTaskForm, taskid=task.task_id, searchForm=searchForm)
                elif "move_to_trash" + str(task.task_id) in request.form:
                    db.session.delete(task)
                    db.session.commit()
                    return redirect(url_for('task'))
                elif "done" + str(task.task_id) in request.form:
                    task.status_id=3
                    project.status_id=3    
                    for t in taskArray:
                        if t.status_id == 1:
                            project.status_id =1
                    db.session.commit()

        if searchForm.submitSearch.data and searchForm.validate_on_submit():
            
            for task in taskArray:
                if task.description.find(searchForm.inputSearchContent.data) != -1 and (task.status_id == searchForm.inputStatus.data or searchForm.inputStatus.data==0 ):    
                    session['content']=searchForm.inputSearchContent.data
                    session['table']="tasks"
                    session['status']=searchForm.inputStatus.data
                    return redirect(url_for('search'))
            flash("No result for '"+ searchForm.inputSearchContent.data +"'")           

                



        if editTaskForm.submitEditTask.data and editTaskForm.validate_on_submit():            
            task=db.session.query(models.Task).filter_by(task_id=session.get('task')).first()
            if (date.fromisoformat(project.deadline)-date.fromisoformat(str(editTaskForm.inputTaskDeadline.data))).days >=0:                
                task.description=editTaskForm.inputTaskDescription.data            
                task.deadline=editTaskForm.inputTaskDeadline.data
                task.priority_id=editTaskForm.inputPriority.data                
                db.session.commit()
            else:
                flash("Task deadline must be done before project deadline")
            

        if form.submit.data and form.validate():
            
            if (date.fromisoformat(project.deadline)-date.fromisoformat(str(form.inputTaskDeadline.data))).days >= 0:
                task = models.Task(description=form.inputTaskDescription.data, 
                                deadline=form.inputTaskDeadline.data,
                               priority_id=form.inputPriority.data,project_id=_projectID, status_id=1)
                db.session.add(task)                
                project.status_id=1 
                db.session.commit()
                return redirect(url_for('task'))
            else:
                flash("Task deadline must be done before project deadline")
        return render_template('task.html',project=project, form=form,editTaskForm=editTaskForm, taskid=None, searchForm=searchForm)
    else:
        return redirect(url_for('userhome'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    editTaskForm = EditTaskForm()
    formx=UD_Task_Form()
    if session.get('table')=='tasks':
        _projectID = session.get('project')
        taskArray = db.session.query(models.Task).filter_by(project_id=_projectID).all()
        taskArr=[]
        for task in taskArray:
            if task.description.find(session.get('content')) != -1 and (task.status_id == session.get('status') or session.get('status')==0 ):
                taskArr.append(task)
        return render_template('search.html',editTaskForm=editTaskForm,taskArr=taskArr,taskid=None)
    else:
        _userId=session.get('user')
        projectArr=[]
        projectArray=db.session.query(models.Project).filter_by(user_id=_userId).all()
        for project in  projectArray:
            if (project.description.find(session.get('content')) != -1 or project.name.find(session.get('content')) != -1) and (project.status_id == session.get('status') or session.get('status')==0): 
                projectArr.append(project)
        return render_template('search.html',editTaskForm=editTaskForm,projectArr=projectArr,taskid=None)


    

    

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5050', debug=True)
