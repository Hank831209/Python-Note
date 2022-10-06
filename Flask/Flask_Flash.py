from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "xxx"

@app.route('/')
def index():
    return render_template('index1.html')

'''
index1.html:

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Index</title>
</head>
<body>
    {% with messages = get_flashed_messages() %}  # 獲取閃現消息
         {% if messages %}
               {% for message in messages %}  # 把消息打印出來
                    <p>{{ message }}</p>
               {% endfor %}
         {% endif %}
    {% endwith %}

<h3>Welcome!</h3>
<a href = "{{ url_for('login') }}">login</a>  # 登入成功的話跳轉到 '/login' 接口
</body>
</html>
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == "POST":
        if request.form['email'] != 'test@gmail.com' or request.form['password'] != 'test':
            error = "Invalid account."
        else:
            flash("Login successfully")
            return redirect(url_for('index'))

    return render_template('login1.html', error=error)  # 登入失敗顯示錯誤訊息

'''
login1.html:
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login</title>
</head>
<body>
    <form method = "post" action = "http://localhost:4000/login">  # 表單送出後導向這個頁面
        <table>
            <tr>
                <td>Email</td>
                <td><input type = 'email' name = 'email'></td>
            </tr>
            <tr>
                <td>Password</td>
                <td><input type = 'password' name = 'password'></td>
            </tr>
            <tr>
                <td><input type = "submit" value = "Submit"></td>
            </tr>
        </table>
    </form>

    {% if error %}
        <p><strong>Error</strong>: {{ error }}</p>  # 提交錯誤時顯示錯誤訊息
    {% endif %}
</body>
</html>
'''
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True) 