from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)

app.config['SECRET_KEY']='thisverysecreatdontsharewithanyone'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////c/Work/sqldb/todo.db'

db= SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    public_id=db.Column(db.String(50),unique=True)
    name=db.Column(db.String(50))
    password=db.Column(db.String(80))
    admin=db.Column(db.Boolean)

class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    text=db.Column(db.String(50))



if __name__=='__main__':
    app.run(debug=True)