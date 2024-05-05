from flask import Flask
from celery import Task
from application.database import db ,  jwt, User , IssuedTo, cach
from application.config import LocalDevelopmentConfig
from flask_cors import CORS
from werkzeug.security import check_password_hash , generate_password_hash
from application import jobs 
from datetime import datetime 



app = Flask(__name__)
app.config.from_object(LocalDevelopmentConfig)
CORS(app)
db.init_app(app)
jwt.init_app(app)
cach.init_app(app)
celery = jobs.celery

class ContextTask(Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return super().__call__( *args, **kwargs)
        
celery.Task = ContextTask

with app.app_context():
    db.create_all()
    # iss = IssuedTo.query.first()
    # iss.return_date = datetime.now()
    if User.query.filter_by(role = "librarian").count() == 0:
        pasw = generate_password_hash("sajalgarg")
        us = User(username = "sajal" , password = pasw , role = "librarian", number_of_books = 0)    
        db.session.add(us)
    db.session.commit()








from application import controller
