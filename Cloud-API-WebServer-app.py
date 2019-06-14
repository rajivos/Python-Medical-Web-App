from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
import itertools
import os



app = Flask(__name__)
Bootstrap(app)
basedir = os.path.abspath(os.path.dirname(__file__))
''' This is the old connection string'''
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
USER   = 'root'
PASS   = ''
HOST   = '35.189.59.219'
DBNAME = 'medicAppdatabase'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/medicAppdatabase'.format(USER,PASS,HOST,DBNAME)
db = SQLAlchemy(app)
ma = Marshmallow(app)

# declaring our model, here is ORM in its full glory

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)


    def __init__(self, username, email):
        self.username = username
        self.email = email


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('username', 'email')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/')
def homepage():   
    return render_template("index.html")




# endpoint to create new user
@app.route("/user", methods=["POST"])
def add_user():
   
    username = request.form.get('title')
    email = request.form.get('mail')
    
    new_user = User(username, email)
    if request.method == 'POST':
        db.session.add(new_user)
        db.session.commit()
        # Failure to return a redirect or render_template
        return 'OK'
    else:
        return render_template('index.html')
    

# endpoint to show all users
@app.route("/user", methods=["GET"])
def get_user():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)


# endpoint to get user detail by id
@app.route("/user/<id>", methods=["GET"])
def user_detail(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


# endpoint to update user
@app.route("/user/<id>", methods=["PUT"])
def user_update(id):
    user = User.query.get(id)
    username = request.json['username']
    email = request.json['email']

    user.email = email
    user.username = username

    db.session.commit()
    return user_schema.jsonify(user)


# endpoint to delete user
@app.route("/user/<id>", methods=["DELETE"])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)



# will 0.0.0.0 work with RMIT's network?
if __name__ == '__main__':
    app.run(host='0.0.0.0')
