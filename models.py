# encoding:utf-8

from exts import db


class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    telephone = db.Column(db.String(11),nullable=False)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100),nullable=False)

    questions = db.relationship('Question', backref='users')


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text,nullable=False)
    time = db.Column(db.DateTime,nullable=False)
    use_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class NewHouse(db.Model):
    __tablename__ = 'newhouse'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    city = db.Column(db.String(50),nullable=False)
    district = db.Column(db.String(100))
    town = db.Column(db.String(100))
    address = db.Column(db.Text)
    building_name=db.Column(db.String(100),nullable=False)
    price = db.Column(db.String(100),nullable=False)
    status = db.Column(db.String(20))


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    question_id = db.Column(db.Integer,db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    question = db.relationship('Question',backref = db.backref('comments'))
    author = db.relationship('User',backref = db.backref('answers'))



