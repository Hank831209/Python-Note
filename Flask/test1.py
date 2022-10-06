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


app = Flask(__name__)

# MySql datebase
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:0983760795@127.0.0.1:3306/test"
app.secret_key = "xxx"
db = SQLAlchemy(app)

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
    if form.validate_on_submit():  # 傳入重複的會報錯
        form_data['name'] = request.form.get('name')                             # sss <class 'str'>
        form_data['tel'] = request.form.get('tel')                               # 0987635241 <class 'str'>
        form_data['num_people'] = request.form.get('num_people')                         # 1 <class 'str'>
        form_data['reserve_date'] = request.form.get('reserve_date')             # 2022-10-15 <class 'str'>
        form_data['AM_PM'] = request.form.get('AM_PM')                           # 下午 <class 'str'>
        form_data['option'] = request.form.get('option')                         # 紀念方案 ＄8,888 <class 'str'>
        form_data['plus'] = request.form.get('plus')                             # 外加入鏡 $500/人(爸媽以外成員) <class 'str'>
        # ----------------------------------------------------------------------------------------------------------------------------------
        # user_id = line_bot_api.get_profile('<user_id>')
        user_id = '123'
        reserve_date = (form_data['reserve_date'] + ' AM' if form_data['AM_PM'] == '上午' else form_data['reserve_date'] + ' PM')
        option = _option_id[form_data['option']]
        # 資進行完處理後存入預約資料

        record = Reserve(user_id=user_id, name=form_data['name'], tel=form_data['tel'], 
                         reserve_date=reserve_date, option=option, plus=form_data['plus'], 
                         record_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S %p'))
        db.session.add(record)
        db.session.commit()
        return render_template('thankyou.html', form_data=form_data)
    else:
        print('輸入失敗 請重新填寫')
        flash("輸入失敗 請重新填寫")
        return render_template('reserve.html', form=form)  # 繼續留在該頁面


@app.route('/create')
def create():
    # Create data
    db.create_all()
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)