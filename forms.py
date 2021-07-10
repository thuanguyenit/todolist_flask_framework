from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired
import wtforms


class SignUpForm(FlaskForm):
    inputFirstName = wtforms.StringField('First name', [DataRequired(message='Please enter your first name!')])
    inputLastName = wtforms.StringField('Last name', [DataRequired(message='Please enter your last name!')])
    inputEmail = wtforms.StringField('Email address', [Email(message='Not availed email address!'),
                                                       DataRequired(message='Please enter your email!!')], )
    inputPassword = wtforms.PasswordField('Password', [DataRequired(message='Enter your pass word!'),
                                                       EqualTo('inputConfirmPassword',
                                                               message="Password does not match")])
    inputConfirmPassword = wtforms.PasswordField('Confirm Password')
    submit = wtforms.SubmitField('Sign Up')


class SignInForm(FlaskForm):
    inputEmail = wtforms.StringField('Email address', [Email(message='Not availed email address!'),
                                                       DataRequired(message='Please enter your email!!')], )
    inputPassword = wtforms.PasswordField('Password', [DataRequired(message='Enter your pass word!')])
    submit = wtforms.SubmitField('Sign In')


class AddTaskForm(FlaskForm):
    inputTaskDescription = wtforms.StringField('Task description', [DataRequired(message='Please enter your task!')])
    inputTaskDeadline = wtforms.DateField('Task deadline', [DataRequired(message='Format: y/m/d')], format='%Y-%m-%d')
    inputPriority = wtforms.SelectField('Priority level', coerce=int)
    submit = wtforms.SubmitField('Add Task')

class AddProjectForm(FlaskForm):
    inputProjectName = wtforms.StringField('Project name', [DataRequired(message='Please enter your project name!')])
    inputProjectDescription = wtforms.StringField('Project description', [DataRequired(message='Please enter your project description!')])
    inputProjectDeadline = wtforms.DateField('Project deadline', [DataRequired(message='Format: y-m-d')], format='%Y-%m-%d')
    submit = wtforms.SubmitField('Add Project')

class EditProjectForm(FlaskForm):
    inputProjectName = wtforms.StringField('Project name', [DataRequired(message='Please enter your project name!')])
    inputProjectDescription = wtforms.StringField('Project description', [DataRequired(message='Please enter your project description!')])
    inputProjectDeadline = wtforms.DateField('Project deadline', [DataRequired(message='Format: y-m-d')], format='%Y-%m-%d')
    submitEditProject = wtforms.SubmitField('done')

class UD_Task_Form(FlaskForm):
    updateTask = wtforms.SubmitField("✏")
    deleteTask = wtforms.SubmitField("❌")

class EditTaskForm(FlaskForm):
    inputTaskDescription = wtforms.StringField('Task description', [DataRequired(message='Please enter your task!')])
    inputTaskDeadline = wtforms.DateField('Task deadline', [DataRequired(message='Format: y-m-d')], format='%Y-%m-%d')
    inputPriority = wtforms.SelectField('Priority level', coerce=int)
    submitEditTask = wtforms.SubmitField('✔')

class SearchForm(FlaskForm):
    inputSearchContent = wtforms.StringField('Search content', [DataRequired(message='Please enter your key-word')])
    inputStatus=wtforms.SelectField('status',coerce=int)
    submitSearch=wtforms.SubmitField('🔍')
    
