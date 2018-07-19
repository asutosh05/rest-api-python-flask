from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash,check_password_hash

app=Flask(__name__)

app.config['SECRET_KEY']='thisverysecreatdontsharewithanyone'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'

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


@app.route('/user',methods=['GET'])
def get_all_user():
    users=User.query.all()
    output=[]
    for user in users:
        user_data={}
        user_data['public_id']=user.public_id
        user_data['name']=user.name
        user_data['password']=user.password
        user_data['admin']=user.admin
        output.append(user_data)
    return jsonify({"users":output})

@app.route('/user/<public_id>',methods=['GET'])
def get_one_user(public_id):
    user=User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message':'no user found'})
    
    user_data={}
    user_data['public_id']=user.public_id
    user_data['name']=user.name
    user_data['password']=user.password
    user_data['admin']=user.admin

    return jsonify({'user':user_data})

@app.route('/user',methods=['POST'])
def create_user():
    data=request.get_json()
    hashed_password=generate_password_hash(data['password'],method='sha256')
    new_user=User(public_id=str(uuid.uuid4()),name=data['name'],password=hashed_password,admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message':'new user created'})

@app.route('/user/<public_id>',methods=['PUT'])
def promte_user(public_id):
    user=User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message':'no user found'})
    
    user.admin=True
    db.session.commit()
    return jsonify({'message':'user promoted to admin'})

@app.route('/user/<public_id>',methods=['DELETE'])
def delete_user(public_id):
    user=User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message':'no user found'})

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message':'user deleted'})



if __name__=='__main__':
    app.run(debug=True)