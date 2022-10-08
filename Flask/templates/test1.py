from email.policy import default
from flask import Flask, abort, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, HiddenField, StringField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField, DateTimeField
from datetime import datetime
# import pymysql
from Table import Reserve, Test_form
import re
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import json


app = Flask(__name__)

# MySql datebase
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:0983760795@127.0.0.1:3306/test"
app.secret_key = "xxx"
db = SQLAlchemy(app)

# 把機密資料寫成txt來讀取, 主要只會用到channelAccessToken和channelSecret
secretFile = json.load(open("secretFile.txt",'r'))
channelAccessToken = secretFile['channelAccessToken']
channelSecret = secretFile['channelSecret']

line_bot_api = LineBotApi(channelAccessToken)
handler = WebhookHandler(channelSecret)


# 標準寫法基本不會改
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    # 紀錄收到過的訊息, 一般不會放
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'


_option_id = {
    (r'純數位檔方案 $4,999'): 1,
    (r'紀念方案 ＄8,888'): 2,
    (r'典藏方案 $13,500'): 3,
    (r'全檔精緻方案 $18,500'): 4,
    (r'成長方案-2年內拍攝3次（可包含新生兒寫真）$19,999'): 5
}

_plus = {
    (r'無'): 1,
    (r'外加入鏡 $500/人(爸媽以外成員)'): 2,
    (r'媽媽另加妝髮造型 $1,000/套'): 3,
    (r'外景拍攝另加 $500-3,000（依地點報價）'): 4,
    (r'新生兒造型 $1,000/套'): 5,
    (r'外景拍攝另加 $500-3,000（依地點報價）'): 6
}

# 資料庫 Table
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
        
        
class Reserve_form(FlaskForm):
    name = StringField('預約姓名', validators=[DataRequired()])
    tel = StringField('預約電話', validators=[DataRequired()])
    num_people = SelectField('預約人數', choices=[('1'), ('2'), ('3'), ('4'), ('5'), ('5人以上')])
    reserve_date =  DateField('預約日期', format='%Y-%m-%d')
    AM_PM = SelectField('預約時間', choices=[('上午'), ('下午')])
    option = SelectField('兒童寫真方案選擇', choices=[choice for choice in _option_id.keys()])
    plus = SelectField('加購項目', choices=[choice for choice in _plus.keys()])
    submit = SubmitField("確認")

        
# home pag
@app.route('/',methods=['GET','POST'])
def index():
    """首頁"""
    form = Reserve_form()
    form_data = dict()  # 感謝表單的回傳值
    Error = list()  # 錯誤訊息
    if form.validate_on_submit():  # 傳入重複的會報錯
        form_data['name'] = request.form.get('name')                             # sss <class 'str'>
        form_data['tel'] = request.form.get('tel')                               # 0987635241 <class 'str'>
        form_data['num_people'] = request.form.get('num_people')                         # 1 <class 'str'>
        form_data['reserve_date'] = request.form.get('reserve_date')             # 2022-10-15 <class 'str'>
        form_data['AM_PM'] = request.form.get('AM_PM')                           # 下午 <class 'str'>
        form_data['option'] = request.form.get('option')                         # 紀念方案 ＄8,888 <class 'str'>
        form_data['plus'] = request.form.get('plus')                             # 外加入鏡 $500/人(爸媽以外成員) <class 'str'>
        # ----------------------------------------------------------------------------------------------------------------------------------
        # 用戶ID處理
        user_id = line_bot_api.get_profile('<user_id>')
        print('user_id: ', user_id)
        user_id = '123'
        
        # 電話處理
        check1 = re.search(pattern=r'^09\d{2}-?\d{3}-?\d{3}$', string=form_data['tel'])  # 手機
        check2 = re.search(pattern=r'^\d{2}-?\d{4}-?\d{4}$', string=form_data['tel'])  # 市話
        check3 = re.search(pattern=r'^\d{3}-?\d{3}-?\d{4}$', string=form_data['tel'])  # 市話
        if (not check1) and (not check2) and (not check3):
            Error.append('預約電話輸入失敗 請重新填寫')

        # 預約日期處理 防止重複
        reserve_date = (form_data['reserve_date'] + ' AM' if form_data['AM_PM'] == '上午' else form_data['reserve_date'] + ' PM')
        if Reserve.query.filter_by(reserve_date=reserve_date).first():  # 是否該時段已被預約
            Error.append('日期輸入失敗 請重新填寫')
            
        # 選擇方案處理
        option = _option_id[form_data['option']]

        if Error:  # 資料有誤
            return render_template('reserve.html', form=form, Error=Error)
        else:      # 資進行完處理後存入資料庫(預約資料)
            record = Reserve(user_id=user_id, name=form_data['name'], tel=form_data['tel'], 
                            num_people=form_data['num_people'], reserve_date=reserve_date, 
                            option=option, plus=form_data['plus'], 
                            record_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S %p'))
            db.session.add(record)
            db.session.commit()
            return render_template('thankyou.html', form_data=form_data)
    else:
        Error.append('輸入失敗 請重新填寫')  # 錯誤訊息
        return render_template('reserve.html', form=form, Error=Error)  # 繼續留在該頁面


@app.route('/create')
def create():
    # Create data
    db.create_all()
    return 'ok'



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)