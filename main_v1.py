from flask import Flask, request, jsonify, render_template,redirect,url_for,session
from chat import ChatBot
import pymysql

# 连接数据库
connection = pymysql.connect(
    host='127.0.0.1',       # 数据库主机地址
    user='rio',            # 数据库用户名
    password='123456',  # 数据库密码
    database='ragkb',  # 数据库名称
    charset='utf8mb4'       # 设置字符集
)

# 创建web app
app = Flask(__name__)
# 实例化聊天机器人
chatbot = ChatBot()
app.secret_key = 'lzy'




@app.errorhandler(404)
def handle_404_error(err):
    return render_template('404.html')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/chat')
def chat():
    if 'username' in session:
        return render_template('chat.html')
    else:
        return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')


    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users WHERE username = %s and password = %s', (username,password))
    
    user = cursor.fetchone()
    cursor.close()

    if user is None:
        return jsonify({'message': '用户名或密码错误'}), 401
    else:
        session['username'] = user[1]
        return jsonify({'message': 'Login successful', 'user': user[1]}), 200
    

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    print("收到注册信息","username:",username,"password:",password)
    cursor = connection.cursor()
    try:
        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(sql, (username, password))
        connection.commit()
        print("记录插入成功！")
        return jsonify({}),200
    except Exception as e:
        # 如果发生错误，回滚事务
        connection.rollback()
        return jsonify({"message": "注册失败,用户名已被使用"}), 401
    finally:
        cursor.close()
        # connection.close()
    
    

@app.route('/question', methods=['POST'])
def question():
    # 获取用户提交的问题
    user_question = request.json.get('question')
    bot_answer = chatbot.reply(user_question)
    
    # 返回问题和答案
    return jsonify({
        'question': user_question,
        'ans': bot_answer
    })


if __name__ == '__main__':
    app.run(debug=True)
