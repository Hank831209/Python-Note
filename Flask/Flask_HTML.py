from flask import Flask, render_template
import poker as p
import model

app = Flask(__name__)


# 定義使用者接口
@app.route('/')
def hello():
    return '<h1>Hello Flask</h1>'  # 可直接回傳HTML語法


@app.route('/hello/<username>')
def hello_someone2(username):
    # 左邊username: 模板裡面有一個變數username
    # 右邊username: python裡面的username
    # 回傳寫好的HTML檔案, 並將HTML檔案中username這變數取代掉, 寫法如下
    # ex: Hello {{ username }} !
    return render_template('index.html', username=username)
'''
index.html:

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    Hello {{ username }} !
</body>
</html>
'''


@app.route('/show_staff')
def hello_google():
    # staff_data = model.getStaff()
    column = ['ID', 'Name', 'DeptId', 'Age', 'Gender', 'Salary']
    staff_data = [['123', 'Hank', '0', '27', 'Man', '878788'], ['124', 'Jerry', '0', '27', 'Man', '878788']]
    return render_template('show_staff.html', staff_data=staff_data, column=column)

# {% ... %} 為程式語法
# {{ ... }} 獲取變數的值
# {# ... #} 註釋
'''
show_staff.html:

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Staff</title>
</head>
<body>
<div>
    <table border="1" width="500">
        <thead>
            <tr>
                {% for c in column %}
                <th>
                    {{ c }}
                </th>
                {% endfor %}
            </tr>
        </thead>
        <tbody>
            {% for emp in staff_data %}
            <tr>
                {% for emp_info in emp %}
                <td>
                    {{ emp_info }}
                </td>
                {% endfor %}
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
</body>
</html>
'''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)