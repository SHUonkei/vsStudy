import sqlite3
from typing import Final, Optional, Union
import unicodedata
import datetime
from flask import Flask, g, redirect, render_template, request, url_for, jsonify, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
import os
from dotenv import load_dotenv
import uuid

# .envファイルの内容を読み込む
load_dotenv()

# データベースのファイル名
DATABASE: Final[str] = os.environ['PATH_TO_DB']

# Flask クラスのインスタンス
app = Flask(__name__, static_folder='templates/static')
app.config["SECRET_KEY"] = os.environ['SECRET_KEY']
# 日本語の文字化け対策
app.json.ensure_ascii = False

class User:
    def __init__(self, id, name, password_hash):
        self.id = id
        self.name = name
        self.password_hash = password_hash

    @staticmethod
    def get(user_id):
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM players WHERE id = ?", (user_id,))
        row = cur.fetchone()
        conn.close()
        if row:
            return User(row['id'], row['name'], row['password'])
        return None

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_email = request.form['email']
        password = request.form['password']
        user = user_authentication(user_email, password)
        if user:
            session['user_id'] = user.id
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('show_user_data')
            return redirect(next_page)
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = str(uuid.uuid4())
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)
        register_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("""
                    INSERT INTO players 
                        (id, name, email, password, date) 
                    VALUES 
                        (?, ?, ?, ?, ?)
                    """, 
                    (user_id, username, email, password_hash, register_date))
        conn.commit()
        conn.close()
        flash('Registration successful', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

def user_authentication(user_email, password):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM players WHERE email = ?", (user_email,))
    row = cur.fetchone()
    conn.close()
    if row and check_password_hash(row['password'], password):
        return User(row['id'], row['name'], row['password'])
    return None

@app.route("/user", methods=["GET"])
def show_user_data():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('mainpage.html', user=User.get(session['user_id']))

@app.route("/logout", methods=["GET"])
def logout():
    session.pop('user_id', None)
    return jsonify({}), 200

@app.errorhandler(403)
def unauthorized_handler(e):
    error_msg = {"errorMessage": "ログインが必須のページです", "statusCode": 403}
    return jsonify(error_msg), 403

from werkzeug.exceptions import HTTPException

@app.errorhandler(HTTPException)
def http_error(e):
    error_msg = {"errorMessage": e.description, "statusCode": e.code}
    return jsonify(error_msg), e.code

# 処理結果コードとメッセージ
RESULT_MESSAGES: Final[dict[str, str]] = {
    'id-has-invalid-charactor': '指定された社員番号には使えない文字があります - 数字のみで指定してください',
    'id-already-exists': '指定された社員番号は既に存在します - 存在しない社員番号を指定してください',
    'id-does-not-exist': '指定された社員番号は存在しません',
    'id-is-manager': '指定された社員番号の社員には部下がいます - 部下に登録された上司を変更してから削除してください',
    'manager-id-has-invalid-charactor': '指定された上司の社員番号には使えない文字があります - 数字のみで指定してください',
    'manager-id-does-not-exist': '指定された上司の社員番号が存在しません - 既に存在する社員番号か追加する社員の社員番号と同じものを指定してください',
    'salary-has-invalid-charactor': '指定された給与には使えない文字があります - 数字のみで指定してください',
    'birth-year-has-invalid-charactor': '指定された生年には使えない文字があります - 数字のみで指定してください',
    'start-year-has-invalid-charactor': '指定された入社年には使えない文字があります - 数字のみで指定してください',
    'name-has-control-charactor': '指定された名前には制御文字があります - 制御文字は指定しないでください',
    'database-error': 'データベースエラー',
    'added': '社員を追加しました',
    'deleted': '削除しました',
    'updated': '更新しました'
}

def get_db() -> sqlite3.Connection:
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception: Optional[BaseException]) -> None:
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def has_control_character(s: str) -> bool:
    return any(map(lambda c: unicodedata.category(c) == 'Cc', s))

@app.route('/')
def index() -> str:
    return render_template('index.html')

@app.route('/studyrecords')
def studyrecords() -> str:
    cur = get_db().cursor()
    e_list = cur.execute(
        """
        SELECT 
            record_id,
            start_time,
            end_time,
            p.name as player_name,
            em.name as educational_material_title,
            s.name as subject_name
        FROM studyrecords sr 
        join players p 
            on p.id=sr.player_id 
        join educational_materials em
            on em.id=sr.educational_material_id
        join subjects s
            on s.id=em.subject_id
        """
    ).fetchall()
    return render_template('studyrecords.html', e_list=e_list)

@app.route('/record-add', methods=['GET', 'POST'])
def record_add() -> str:
    if request.method == 'POST':
        record_id = str(uuid.uuid4())
        subject_id = request.form['subject']
        educational_material_id = request.form['educational_material']
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(hours=1)  # Example: adding 1 hour
        player_id = session.get('user_id')

        if not player_id:
            flash('Please log in to add a record.', 'danger')
            return redirect(url_for('login'))

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO studyrecords 
                (record_id, player_id, educational_material_id, start_time, end_time) 
            VALUES 
                (?, ?, ?, ?, ?)
            """,
            (record_id,player_id, educational_material_id, start_time, end_time)
        )
        conn.commit()
        flash('Record added successfully!', 'success')
        return redirect(url_for('studyrecords'))

    conn = get_db()
    cur = conn.cursor()
    subjects = cur.execute("SELECT id, name FROM subjects").fetchall()
    educational_materials = cur.execute("SELECT id, name FROM educational_materials").fetchall()
    
    return render_template('record-add.html', subjects=subjects, educational_materials=educational_materials)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
