from flask import Flask

app = Flask(__name__)

@app.route('/home')
def index():
    return "Welcome home!"


@app.route('/home1/<name>')
def index1(name):
    return f"Welcome home! {name}!"


@app.route('/home2/<int:age>')  # :後面不能有空格
def index2(age):
    return f"Age: {age}!"


def index3():
    return 'Hello'


app.add_url_rule('/hello', "index3", index3)  # 效果等同於用 @app.route('/hello')去寫

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)