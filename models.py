from sqlalchemy.orm import relationship

from main import db
from sqlalchemy import Sequence, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    user_id = db.Column(db.Integer, Sequence('user_id_seq'), primary_key=True)
    first_name = db.Column(db.String(64), index=True, nullable=False)
    last_name = db.Column(db.String(64), index=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    projects= relationship('Project',back_populates='user')

    def __repr__(self):
        return '<user full name: {} {}, email: {}>'.format(self.first_name, self.last_name, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Task(db.Model):
    task_id = db.Column(db.Integer, Sequence('task_id_seq'), primary_key=True)
    description = db.Column(db.String(255), nullable=False)    
    deadline = db.Column(db.String(255), nullable=False)
    priority_id = db.Column(db.Integer, ForeignKey('priority.priority_id'))  
    project_id = db.Column(db.Integer, ForeignKey('project.project_id'))  
    status_id = db.Column(db.Integer, ForeignKey('status.status_id'))  

    priority = relationship('Priority', back_populates='tasks')
    status= relationship('Status',back_populates='s_tasks')
    project=relationship('Project',back_populates='p_tasks')
    

    def __repr__(self):
        return '<Description: {}, user id: {}>'.format(self.description, self.user_id)

    def getColor(self):
        if self.priority_id==1:
            return "table-hover table-danger"
        else:
            if self.priority_id == 2:
                return "table-hover table-warning"
            else:
                if self.priority_id == 3:
                    return "table-hover table-info"
                else:
                    if self.priority_id == 4:
                        return "table-hover table-primary"



class Priority(db.Model):
    priority_id = db.Column(db.Integer, Sequence('task_id_seq'), primary_key=True)
    text = db.Column(db.String(255), nullable=False)

    tasks = relationship('Task', back_populates='priority')


class Status(db.Model):
    status_id=db.Column(db.Integer, Sequence('status_id_seq'), primary_key=True)
    description=db.Column(db.String(255), nullable=False) 
    
    s_tasks = relationship('Task', back_populates='status')
    s_projects =relationship('Project', back_populates='status')

class Project(db.Model):
    project_id = db.Column(db.Integer, Sequence('project_id_seq'), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    deadline = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('user.user_id')) 
    status_id = db.Column(db.Integer, ForeignKey('status.status_id')) 

    p_tasks= relationship('Task',back_populates='project')
    status = relationship('Status',back_populates='s_projects')
    user = relationship('User',back_populates='projects')