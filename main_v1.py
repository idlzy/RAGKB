from flask import Flask, request, jsonify, render_template,redirect,url_for,session
from flask_cors import CORS
from chat import ChatBot
import pymysql
import os
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
    return redirect(url_for('chat'))

@app.route('/chat')
def chat():
    if 'username' in session:
        return render_template('chat.html')
    else:
        return render_template('login.html')

@app.route('/kb')
def kb():
    if 'username' in session:
        return render_template('kb.html')
    else:
        return render_template('login.html')

CORS(app)  # 允许跨域请求

# 上传文件存储路径
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 允许上传的文件类型
ALLOWED_EXTENSIONS = {'doc', 'docx','pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/LoadFile', methods=['POST'])
def LoadFile():
    # if 'files[]' not in request.files:
    #     return jsonify({'error': '没有文件部分'}), 400
    files = request.files.getlist('files[]')
    print(files)
    if not files:
        return jsonify({'error': '没有选择文件'}), 400

    uploaded_files = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filename)
            uploaded_files.append(file.filename)
        else:
            return jsonify({'error': '文件类型不允许'}), 400

    return jsonify({'message': '文件上传成功', 'files': uploaded_files}), 200

@app.route('/getUploadedFiles')
def getUploadedFiles():
    res = os.listdir("uploads")
    return jsonify({'names': res}), 200

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
    app.run(debug=True,host='0.0.0.0')
