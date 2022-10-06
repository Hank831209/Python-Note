from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/validate', methods=['POST'])
def validate():
    if request.method == 'POST' and request.form['email'] == 'test@gmail.com' and request.form['password'] == 'test':
        return redirect(url_for('success'))  # 重新導向'/success'這個接口

    return redirect(url_for('login'))

@app.route('/success')
def success():
    return 'Logged in successfully.'

'''
login.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login</title>
</head>
<body>
    <form method = "post" action = "http://localhost:4000/validate">  # 提交表單時導向這個網址
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
</body>
</html>
'''
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True) 