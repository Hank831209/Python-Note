from flask import Flask
app = Flask(__name__)  # 創建Flask對象

@app.route('/')  # 路由, 表示"/"用 index這函數來處理
def index():
    return "Hello, flask!";

if __name__ == '__main__':
    # Flask會開啟一個自帶的Web Server
    app.run(host='0.0.0.0', port=4000, debug=True)