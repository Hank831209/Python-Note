from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# /hello_get?name=XXX&age=YYY ---> 希望使用者這樣輸入
@app.route('/hello_get')
def hello_get():
    name = request.args.get('name')  # get使用者輸入的那個參數名稱
    age = request.args.get('age')
    if not name:
        return 'What is your name?'
    elif not age:
        return 'Hello {}.'.format(name)
    else:
        output_html = 'Hello {}, you are {} years old.'
        return output_html.format(name, age)


@app.route('/hello_get2')
def hello_get2():
    name = request.args.get('name')  # get使用者輸入的那個參數名稱
    age = request.args.get('age')
    # 可利用打印輸出的HTML語法來Debug
    # print(render_template('hello_get.html', name=name, age=age))
    return render_template('hello_get.html', name=name, age=age)

'''
hello_get.html:

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    {% if name == None %}
    What's your name?
    {% elif age == None %}
    Hello {{ name }} !
    {% else %}
    Hello {{ name }}, you are {{ age }} years old.
    {% endif %}
</body>
</html>
'''

# methods=['GET', 'POST']定義可使用的方法
@app.route('/hello_post', methods=['GET', 'POST'])
def hello_post():
    output_html = """
    <form action="/hello_post" method="POST">
    <label>What is your name?</label>
    <br>
    <input name="name">
    <button type="submit">SUBMIT</button>
    </form>
    """
    method = request.method  # return "GET" or "POST"
    if method == 'GET':
        return output_html
    elif method == 'POST':
        name = request.form.get('name')
        output_html += '''
        <h1>Hello {}</h1>
        '''.format(name)
        return output_html
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)