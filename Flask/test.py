# form.py
# Flask-WTF Validation example in PyLadies TW Newsletter, October, 2017

from xml.etree.ElementTree import Comment
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, IntegerField, FloatField, DateField, SelectField, SubmitField
from wtforms.validators import InputRequired, DataRequired, Optional, Length, Email, URL,NumberRange, EqualTo, Regexp

app = Flask(__name__)
app.config["SECRET_KEY"] = "hard to guess string"    # Important for CSRF token
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
bootstrap = Bootstrap(app)

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=4,max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6,max=10)])
    confirm  = PasswordField("Repeat Password", validators=[
        InputRequired(),
        Length(min=6,max=10),
        EqualTo('password', "Password must match")])
    email = StringField("Email",validators=[InputRequired(),Email()])
    url = StringField("Your Website",validators=[Optional(),URL()])
    age = IntegerField("How old are you?", validators=[
        InputRequired(),
        DataRequired("Please enter integer")])
    hour = FloatField("How many hours do you sleep?", validators=[
        Optional(),
        NumberRange(0, 24, "The hours should be between %(min)s and %(max)s")])
    mobile = StringField("Mobile Phone Number", validators=[
        InputRequired(), 
        Regexp("^[0][9][0-9]{8}$", message="Invalid Taiwan Mobile Phone number")])
    date = DateField("Start Date, ex: 2017/10/28", format='%Y/%m/%d')
    language = SelectField('Programming Language', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    recaptcha = RecaptchaField()
    submit = SubmitField("Submit")


@app.route("/", methods=["GET", "POST"])
def val():
    form = RegisterForm()
    formData = {
        'username': None,
        'password': None,
        'email': None,
        'url': None,
        'age': None,
        'hour': None,
        'mobile': None,
        'date': None,
        'language': None
    }
    if form.validate_on_submit():
        formData = {
            'username': form.username.data,
            'password': form.password.data,
            'email': form.email.data,
            'url': form.url.data,
            'age': form.age.data,
            'hour': form.hour.data,
            'mobile': form.mobile.data,
            'date': form.date.data.strftime("%Y/%m/%d"),
            'language': form.language.data
        }
        session["formData"] = formData
        return redirect(url_for("val"))
    elif form.errors and 'formData' in session:
        del session['formData']
    return render_template("val.html", form=form, formData=session.get("formData"))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)