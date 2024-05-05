from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_caching import Cache 
from datetime import datetime
from datetime import timedelta





engine = None
Base = declarative_base()
db = SQLAlchemy()
jwt = JWTManager()
cach = Cache()

class User( db.Model ):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    role = db.Column(db.String, nullable = False )
    number_of_books = db.Column(db.Integer)
    last_visit = db.Column(db.DateTime)    
    issue = db.relationship('IssuedTo', backref='user.user_id', cascade = "all, delete")
    request = db.relationship('Request', backref='user.user_id', cascade = "all, delete")
    return_ = db.relationship('Return', backref='user.user_id', cascade = "all, delete")
    feedback = db.relationship('Feedback', backref='user.user_id', cascade = "all, delete")

class Section(db.Model):
    __tablename__ = 'section'
    id = db.Column(db.Integer, autoincrement = True,  primary_key = True)
    name = db.Column(db.String, unique = True)
    description = db.Column(db.String)
    date_created = db.Column(db.DateTime,  default=datetime.utcnow)
    book = db.relationship('Book', backref='section.id', cascade = "all, delete")


class Book(db.Model):
    __tablename__ = 'book'
    id =  db.Column(db.Integer, autoincrement = True,  primary_key = True)
    name = db.Column(db.String, unique = True)
    content = db.Column(db.String)
    author = db.Column(db.String)
    book_ = db.Column(db.String)
    section = db.Column(db.Integer, db.ForeignKey('section.id'))
    issue = db.relationship('IssuedTo', backref='book.id', cascade = "all, delete")
    return_ = db.relationship('Return', backref='book.id', cascade = "all, delete")
    request = db.relationship('Request', backref='book.id', cascade = "all, delete")
    feedback = db.relationship('Feedback', backref='book.id', cascade = "all, delete")


class Request(db.Model):
    __tablename__ = 'Request'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id')  )


class Return(db.Model):
    __tablename__ = 'Return'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id') )


 

class IssuedTo(db.Model):
    __tablename__ = 'issued'
    id = db.Column(db.Integer, autoincrement = True,  primary_key = True)    
    date_issued = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(days=7))
    issued_book = db.Column(db.Integer , db.ForeignKey('book.id'))
    issued_user = db.Column(db.Integer , db.ForeignKey('user.user_id'))

class IssuedData(db.Model):
    __tablename__ = 'issueddata'
    id = db.Column(db.Integer, autoincrement = True,  primary_key = True)    
    date_issued = db.Column(db.DateTime, default=datetime.utcnow)
    issued_book = db.Column(db.Integer , db.ForeignKey('book.id'))
    issued_user = db.Column(db.Integer , db.ForeignKey('user.user_id'))

class Feedback(db.Model):
    __tablename__ = "feedback"
    f_id = db.Column(db.Integer, autoincrement = True,  primary_key = True)
    feed = db.Column(db.String)
    user_id =  db.Column(db.Integer, db.ForeignKey('user.user_id'))
    book_id =  db.Column(db.Integer, db.ForeignKey('book.id') )   






