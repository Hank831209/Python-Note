from flask import Flask, render_template, make_response, session

app = Flask(__name__)
app.secret_key = "test"

@app.route('/session', methods=['GET'])
def sess():
    resp = make_response("<html><body>Session.<a href='/getValue'>Get Value</a></body></html>")  # 顯示傳該網頁
    session['name'] = 'Hank'  # 存在服務器端
    return resp

@app.route('/getValue')
def getValue():
    if 'name' in session:
        name = session['name']
        return render_template('getvalue.html', name=name)

'''
getvalue.html:

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>GetValue</title>
</head>
<body>
<p>Session value: <b> {{ name }} </b> </p>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True) 