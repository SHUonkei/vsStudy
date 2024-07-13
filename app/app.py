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
app = Flask(__name__, static_folder='static')
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
        file = request.files['icon']
        file.save(os.path.join('./static/icon', file.filename))

        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("""
                    INSERT INTO players 
                        (id, name, email, password, date, icon_path) 
                    VALUES 
                        (?, ?, ?, ?, ?, ?)
                    """, 
                    (user_id, username, email, password_hash, register_date, file.filename))
        
        record_id = str(uuid.uuid4())
        cur.execute("""
                    INSERT INTO achievements
                        (id,player_id, total_study_time, total_win, total_lose, total_draw)
                    VALUES
                        (?,?, 0, 0, 0, 0)
                    """,
                    (record_id,user_id,))
        
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
    return redirect(url_for('index'))

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
    if 'user_id' not in session:
        flash('ログインしてください.', 'success')
        return redirect(url_for('login'))
    if request.method == 'POST':
        record_id = str(uuid.uuid4())
        educational_material_id = request.form['educational_material']

        start_time = request.form['start_time']
        end_time = request.form['end_time']

        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%dT%H:%M')

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
        
        # Update total study time
        # 分単位で記録
        total_study_time = (end_time - start_time).total_seconds() / 60
        cur.execute(
            """
            UPDATE achievements
            SET total_study_time = total_study_time + ?
            WHERE player_id = ?
            """,
            (total_study_time, player_id)
        )
        
        conn.commit()
        flash('Record added successfully!', 'success')
        return redirect(url_for('studyrecords'))

    conn = get_db()
    cur = conn.cursor()
    subjects = cur.execute("SELECT id, name FROM subjects").fetchall()
    educational_materials = cur.execute("SELECT id, name FROM educational_materials").fetchall()
    
    return render_template('record-add.html', subjects=subjects, educational_materials=educational_materials)

@app.route('/materials')
def materials() -> str:
    cur = get_db().cursor()
    e_list = cur.execute(
        """
        SELECT 
            em.name as educational_material_title,
            s.name as subject_name
        FROM educational_materials em
        join subjects s
            on s.id=em.subject_id
        """
    ).fetchall()
    return render_template('materials.html', e_list=e_list)

@app.route('/material-add', methods=['GET', 'POST'])
def material_add() -> str:
    if 'user_id' not in session:
        flash('ログインしてください.', 'success')
        return redirect(url_for('login'))
    if request.method == 'POST':
        record_id = str(uuid.uuid4())
        material_title = request.form['material_title']
        subject_id = request.form['subject_id']
        
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO educational_materials 
                (id, name, subject_id) 
            VALUES 
                (?, ?, ?)
            """,
            (record_id, material_title, subject_id)
        )
        conn.commit()
        flash('Record added successfully!', 'success')
        return redirect(url_for('materials'))

    conn = get_db()
    cur = conn.cursor()
    subjects = cur.execute("SELECT id, name FROM subjects").fetchall()
    
    return render_template('material-add.html', subjects=subjects)

@app.route('/subjects')
def subjects() -> str:
    cur = get_db().cursor()
    e_list = cur.execute(
        """
        SELECT 
            s.name as subject_name
        FROM subjects s
        """
    ).fetchall()
    return render_template('subjects.html', e_list=e_list)

@app.route('/subject-add', methods=['GET', 'POST'])
def subject_add() -> str:
    if 'user_id' not in session:
        flash('ログインしてください.', 'success')
        return redirect(url_for('login'))
    if request.method == 'POST':
        record_id = str(uuid.uuid4())
        subject_title = request.form['subject_title']
        
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO subjects 
                (id, name) 
            VALUES 
                (?, ?)
            """,
            (record_id, subject_title)
        )
        conn.commit()
        flash('Record added successfully!', 'success')
        return redirect(url_for('subjects'))

    conn = get_db()
    cur = conn.cursor()
    subjects = cur.execute("SELECT id, name FROM subjects").fetchall()
    
    return render_template('subject-add.html', subjects=subjects)

@app.route('/ranking')
def ranking() -> str:
    cur = get_db().cursor()
    e_list = cur.execute(
        """
        SELECT 
            p.name,
            p.icon_path,
            a.total_study_time,
            a.total_win,
            a.total_lose,
            a.total_draw
        FROM players p
        JOIN achievements a
        ON p.id = a.player_id
        """
    ).fetchall()

    # Sort e_list based on the rules
    sorted_e_list = sorted(
        e_list,
        key=lambda x: x[ 'total_study_time' ] * ( x['total_win'] / (x['total_draw'] + x['total_win'] + x['total_lose'] + 0.1)),
        reverse=True
    )

    # Assign ranks
    ranked_e_list = []
    rank = 1
    for index, player in enumerate(sorted_e_list):
        rank = index + 1
        rate = player['total_study_time']*player['total_win'] / (player['total_draw'] + player['total_win'] + player['total_lose'] + 0.1)
        ranked_e_list.append((rank, rate, player))

    return render_template('ranking.html', ranked_e_list=ranked_e_list)

@app.route('/challenge', methods=['GET', 'POST'])
def challenge():
    if 'user_id' not in session:
        flash('ログインしてください.', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        battle_id = str(uuid.uuid4())
        player_id = session['user_id']
        opponent_id = request.form['opponent_id']
        battle_date = datetime.datetime.now()
        start_time = battle_date
        end_time = None
        winner_id = None
        current_state = 'pending'
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO battles 
                (id, player_id, opponent_id, date, start_time, end_time, winner_id, current_state) 
            VALUES 
                (?, ?, ?, ?, ?, ?, ?, ?)
            """, 
            (battle_id, player_id, opponent_id, battle_date, start_time, end_time, winner_id, current_state))
        conn.commit()
        conn.close()
        
        flash('Challenge sent successfully!', 'success')
        return redirect(url_for('challenges'))
    
    conn = get_db()
    cur = conn.cursor()
    players = cur.execute("SELECT id, name FROM players WHERE id != ?", (session['user_id'],)).fetchall()
    conn.close()
    
    return render_template('challenge.html', players=players)


@app.route('/challenges')
def challenges():
    if 'user_id' not in session:
        flash('ログインしてください.', 'danger')
        return redirect(url_for('login'))
    
    conn = get_db()
    cur = conn.cursor()
    challenges = cur.execute(
        """
        SELECT 
            b.id, 
            b.date,
            b.player_id,
            b.opponent_id,
            b.current_state,
            p1.name AS player_name, 
            p2.name AS opponent_name,
            b.winner_id 
        FROM battles b
        JOIN players p1 ON b.player_id = p1.id
        JOIN players p2 ON b.opponent_id = p2.id
        WHERE b.opponent_id = ? OR b.player_id = ?
        """,
        (session['user_id'], session['user_id'])).fetchall()
    conn.close()
    
    return render_template('challenges.html', challenges=challenges)


@app.route('/accept-challenge/<battle_id>', methods=['POST'])
def accept_challenge(battle_id):
    if 'user_id' not in session:
        flash('ログインしてください.', 'danger')
        return redirect(url_for('login'))
    
    conn = get_db()
    cur = conn.cursor()
    
    battle = cur.execute("SELECT * FROM battles WHERE id = ?", (battle_id,)).fetchone()
    if not battle:
        flash('Challenge not found.', 'danger')
        return redirect(url_for('challenges'))
    
    if battle['opponent_id'] != session['user_id']:
        flash('You are not authorized to accept this challenge.', 'danger')
        return redirect(url_for('challenges'))
    
    cur.execute("""
        UPDATE battles 
        SET current_state = ?
        WHERE id = ?
    """, ('playing', battle_id)
    )
    conn.commit()
    conn.close()
    
    flash('Challenge accepted!', 'success')
    return redirect(url_for('challenges'))

@app.route('/finish-challenge/<battle_id>', methods=['POST'])
def finish_challenge(battle_id):
    if 'user_id' not in session:
        flash('ログインしてください.', 'danger')
        return redirect(url_for('login'))
    
    conn = get_db()
    cur = conn.cursor()
    
    battle = cur.execute("SELECT * FROM battles WHERE id = ?", (battle_id,)).fetchone()
    if not battle:
        flash('Challenge not found.', 'danger')
        return redirect(url_for('challenges'))
    
    if battle['opponent_id'] != session['user_id']:
        flash('You are not authorized to accept this challenge.', 'danger')
        return redirect(url_for('challenges'))
    
    # Calculate study times for the day
    today = datetime.date.today()
    player_study_time = cur.execute("""
        SELECT SUM(julianday(end_time) - julianday(start_time)) * 24
        FROM studyrecords 
        WHERE player_id = ? AND date(start_time) = ?
    """, (battle['player_id'], today)).fetchone()[0] or 0
    
    opponent_study_time = cur.execute("""
        SELECT SUM(julianday(end_time) - julianday(start_time)) * 24
        FROM studyrecords 
        WHERE player_id = ? AND date(start_time) = ?
    """, (battle['opponent_id'], today)).fetchone()[0] or 0
    
    winner_id = None
    loser_id = None
    if player_study_time > opponent_study_time:
        winner_id = battle['player_id']
        loser_id = battle['opponent_id']
    elif opponent_study_time > player_study_time:
        winner_id = battle['opponent_id']
        loser_id = battle['player_id']
    
    cur.execute("""
        UPDATE battles 
        SET end_time = ?, winner_id = ?, current_state = ?
        WHERE id = ?
    """, (datetime.datetime.now(), winner_id,'finish', battle_id))

    # Update achievements
    if winner_id:
        cur.execute("""
            UPDATE achievements 
            SET total_win = total_win + 1
            WHERE player_id = ?
        """, (winner_id,))
        
        cur.execute("""
            UPDATE achievements 
            SET total_lose = total_lose + 1
            WHERE player_id = ?
        """, (loser_id,))
        
    else:
        cur.execute("""
            UPDATE achievements 
            SET total_draw = total_draw + 1
            WHERE player_id = ?
        """, (battle['player_id'],))
        cur.execute("""
            UPDATE achievements 
            SET total_draw = total_draw + 1
            WHERE player_id = ?
        """, (battle['opponent_id'],))

    conn.commit()
    conn.close()
    
    flash('Challenge completed!', 'success')
    return redirect(url_for('challenges'))


if __name__ == '__main__':
    app.run(port=5000, debug=True)
