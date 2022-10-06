from flask import Flask, request, jsonify, render_template
import poker as p
import model
# jsonify 把字典或list轉成json字串
# render_template 寫成Jinja2模板(HTML), 可直接帶入, 但python本身語法也做得到, 視情況使用

# , static_folder='./static2'  # 本地端的folder可以改名稱
# static_url_path='/resource'  # 網頁端的static可以換名稱
app = Flask(__name__, static_folder='./static')


# 定義使用者接口
@app.route('/')
def hello():
    return '<h1>Hello Flask</h1>'


@app.route('/hello/<username>')
def hello_someone(username):
    output_html = 'Hello {} !'
    return output_html.format(username)


@app.route('/hello2/<username>')
def hello_someone2(username):
    # 左邊username: 模板裡面有一個變數username
    # 右邊username: python裡面的username
    # 回傳寫好的HTML檔案, 並將HTML檔案中username這變數取代掉, 寫法如下
    # ex: Hello {{ username }} !
    return render_template('index.html', username=username)


@app.route('/add/<x>/<y>')
def two_sum(x, y):
    add_num = str(int(x) + int(y))
    return '<h1> 相加結果為: {} </h1>'.format(add_num)


@app.route('/auth', methods=['POST'])  # ?
def auth():
    return "token"


# @app.route('/emp/<br_number>/<dep_number>')
# def emp(br_number, dep_number):
#     sql = """
#     select emp_name, emp_number from emp
#     where br_number='{}' and dep_number='{}'
#     """.format(br_number, dep_number)
#     output = conn.execute(sql)
#     return to_json(output)

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


# # 把洗牌的程式包成API
# # /poker?player=5
# @app.route('/poker')
# def play_poker():
#     player = int(request.args.get('player'))
#     output_json = p.poker(player)
#     return jsonify(output_json)


@app.route('/poker', methods=['GET', 'POST'])
def poker():
    request_method = request.method
    players = 0
    cards = dict()
    if request_method == 'POST':
        players = int(request.form.get('players'))
        cards = p.poker(players)  # 依人數隨機發牌, json格式
    return render_template('poker.html', request_method=request_method, cards=cards)


@app.route('/show_staff')
def hello_google():
    staff_data = model.getStaff()
    column = ['ID', 'Name', 'DeptId', 'Age', 'Gender', 'Salary']
    return render_template('show_staff.html', staff_data=staff_data,
                                              column=column)


if __name__ == '__main__':
    # debug=True --->
    app.run(debug=True, host='0.0.0.0', port=5000)  # '0.0.0.0' ---> 可透過任一IP來訪問服務









