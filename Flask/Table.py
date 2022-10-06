from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, HiddenField, StringField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField

app = Flask(__name__)
# MySql datebase
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:0983760795@127.0.0.1:3306/test"
db = SQLAlchemy(app)

class Reserve(db.Model):
    __tablename__ = 'Reserve'
    reserve_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(33))
    name = db.Column(db.String(25), nullable=False)
    tel = db.Column(db.String(14), nullable=False)
    num_people = db.Column(db.String(5), nullable=False)
    reserve_date = db.Column(db.String(30))  # Check
    option = db.Column(db.Integer)
    plus = db.Column(db.String(100))
    record_date = db.Column(db.String(30))  # Check

    def __init__(self, user_id, name, tel, num_people, reserve_date, option, plus, record_date):
        self.user_id = user_id
        self.name = name
        self.tel = tel
        self.num_people = num_people
        self.reserve_date = reserve_date
        self.option = option
        self.plus = plus
        self.record_date = record_date

class Member(db.Model):
    __tablename__ = 'Member'
    member_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), nullable=False)
    tel = db.Column(db.String(14), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.String(33))

    def __init__(self, name, tel, email, user_id):
        self.name = name
        self.tel = tel
        self.email = email
        self.user_id = user_id
        

class Scheme(db.Model):
    __tablename__ = 'Scheme'
    option_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _class = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(100))

    def __init__(self, option_id, _class, name, price, content):
        self.option_id = option_id
        self._class = _class
        self.name = name
        self.price = price
        self.content = content

class Test_form(db.Model):
    __tablename__ = 'Test_form'
    name = db.Column(db.String(100), primary_key=True)
    ph_number = db.Column(db.String(100), nullable=False)
    people = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(100))
    option = db.Column(db.String(100))
    plus = db.Column(db.String(100))
    

    def __init__(self, name, ph_number, people, date, time, option, plus):
        self.name = name
        self.ph_number = ph_number
        self.people = people
        self.date = date
        self.time = time
        self.option = option
        self.plus = plus
    

@app.route('/create')
def create():
    # Create data
    db.create_all()

    return 'create ok'


# 新增資料
@app.route('/insert')
def insert1():
    # Add data
    now = datetime.now()
    record_date = now.strftime('%Y-%m-%d %p')  # 字串 2022-10-06 PM
    print(record_date, type(record_date))
    record = Reserve(user_id='456', name='456', tel='48998156', people='5', 
                         reserve_date=record_date, option='4564', plus='546', record_date=record_date)
    db.session.add(record)
    db.session.commit()
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)