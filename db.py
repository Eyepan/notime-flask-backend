from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import UUIDType
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(UUIDType(binary=False), primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    notebooks = db.relationship('Notebook', backref='user', lazy=True)

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', password='{self.password}')"


class Notebook(db.Model):
    id = db.Column(UUIDType(binary=False), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    pages = db.relationship('Page', backref='notebook', lazy=True)

    def __repr__(self):
        return f"Notebook(id={self.id}, user_id={self.user_id}, title='{self.title}')"


class Page(db.Model):
    id = db.Column(UUIDType(binary=False), primary_key=True)
    notebook_id = db.Column(db.Integer, db.ForeignKey(
        'notebook.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Page(id={self.id}, notebook_id={self.notebook_id}, title='{self.title}', content='{self.content}')"


app.app_context().push()

db.create_all()
