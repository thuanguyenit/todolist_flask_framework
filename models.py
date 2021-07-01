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

    tasks = relationship('Task', back_populates='user')

    def __repr__(self):
        return '<user full name: {} {}, email: {}>'.format(self.first_name, self.last_name, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



class Priority(db.Model):
    priority_id = db.Column(db.Integer, Sequence('task_id_seq'), primary_key=True)
    text = db.Column(db.String(255), nullable=False)

    tasks = relationship('Task', back_populates='priority')


class Task(db.Model):
    task_id = db.Column(db.Integer, Sequence('task_id_seq'), primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255), nullable=False)  # Accept value: "running" or "completed" or "trash"
    user_id = db.Column(db.Integer, ForeignKey('user.user_id'))
    priority_id = db.Column(db.Integer, ForeignKey('priority.priority_id'))

    user = relationship('User', back_populates='tasks')

    priority = relationship('Priority', back_populates='tasks')

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




