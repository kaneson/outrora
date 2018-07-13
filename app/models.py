from . import db
from datetime import datetime
from flask_login import UserMixin

from werkzeug.security import check_password_hash, generate_password_hash
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), index=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hashed = db.Column(db.String(128))
    todos = db.relationship('Todo', backref='user', lazy='dynamic')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def password(self):
        raise AttributeError('A senha não é um atributo com permissão de leitura')
    
    @password.setter
    def password(self, password):
        self.password_hashed = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hashed, password)
        
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(20), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))