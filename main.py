from flask import Flask, redirect, session, request, render_template, flash, url_for
from sqlalchemy.orm import Session


from forms import SignUpForm, SignInForm, AddTaskForm, UD_Task_Form, EditTaskForm
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
    form = AddTaskForm()
    _userId = session.get('user')
    editTaskForm=EditTaskForm()
    formx=UD_Task_Form()
    edit=False


    if _userId:
        user = db.session.query(models.User).filter_by(user_id=_userId).first()
        form.inputPriority.choices = [(p.priority_id, p.text) for p in db.session.query(models.Priority).all()]
        editTaskForm.inputPriority.choices = [(p.priority_id, p.text) for p in db.session.query(models.Priority).all()]

        taskArray= db.session.query(models.Task).filter_by(user_id=_userId).all()

        if formx.validate_on_submit():
            for task in taskArray:
                if "update"+str(task.task_id) in request.form:
                    session['task'] = task.task_id
                    return render_template('userhome.html', form=form, user=user,editTaskForm=editTaskForm, taskid=task.task_id)
                elif "move_to_trash" + str(task.task_id) in request.form:
                    task.status = "trash"
                    db.session.commit()
                    return redirect(url_for('userhome'))
                elif "done" + str(task.task_id) in request.form:
                    task.status="done"
                    db.session.commit()




        if editTaskForm.submitEditTask.data and editTaskForm.validate():
            task = db.session.query(models.Task).filter_by(task_id=session.get('task')).first()
            task.description = editTaskForm.inputTaskDescription.data
            task.priority_id = editTaskForm.inputPriority.data
            db.session.commit()

        if form.submit.data and form.validate():
            task = models.Task(description=form.inputTaskDescription.data, user_id=_userId,
                               priority_id=form.inputPriority.data, status="running")
            db.session.add(task)
            db.session.commit()



            return redirect(url_for('userhome'))
        return render_template('userhome.html', form=form, user=user, editTaskForm=editTaskForm, taskid=None)
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

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8080', debug=True)
