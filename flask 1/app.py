import sqlite3, os
from flask import Flask, render_template, request, url_for, flash, redirect, g
from DataBase import DataBase
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = '/tmp/database.db'
DEBUG = True
SECRET_KEY = 'gadsgsf123&81230><asd,'
MAX_CONTENT_LENGTH = 1024*1024
app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'database.db')))

dbase = None
@app.before_request
def before_request():
     global dbase
     db = get_db()
     dbase = DataBase(db)

login_manager = LoginManager(app)
@login_manager.user_loader #Загрузка пользователя 
def load_user(user_id):
    return UserLogin().fromDB(user_id, dbase)

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    db = connect_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.route("/")
def index():
    path = url_for('static', filename='img/robot.jpg')
    path1 = url_for('static', filename='img/ruk.jpg')
    path2 = url_for('static', filename='img/robot2.jpg')
    path3 = url_for('static', filename='php/sender.php')
    is_admin = None
    if str(current_user.is_authenticated)!='False':
        is_admin = int(current_user.get_admin())
    else:
        is_admin = None

    return render_template(
        'index.html',
        tecnol=dbase.getTechnJSON(),
        posts=dbase.getJSON(),
        path=path,
        path1=path1,
        path2=path2,
        path3=path3,
        auth_user=str(current_user.is_authenticated),
        is_admin=is_admin
    )

@app.route("/update_status", methods= ["POST", "GET"])
@login_required
def updateStatus():
    tmp = None
    menu = None
    if int(current_user.get_admin()) == 1:
        tmp = 'admin.html'
        menu = dbase.getJSON()
        if request.method == "POST":
            res = dbase.updateStatus(request.form['title'], request.form['content'], request.form['status'], request.form['id'])
            if not res:
                flash('Ошибка обновления статуса', category= 'error')
            else:
                flash('Статус успешно обновлен', category='success')
    else:
        tmp = 'error_admin.html'
    return render_template(tmp, menu=menu)


@app.route("/add_post", methods= ["POST", "GET"])
@login_required
def addPost():
    if request.method == "POST":
        res = None
        if int(current_user.get_admin()) == 1:
            res = dbase.addPost(request.form['title'], request.form['content'], current_user.get_id(), 'public')
        else:
            res = dbase.addPost(request.form['title'], request.form['content'], current_user.get_id(), 'draft')
        if not res:
            flash('Ошибка добавления статьи', category= 'error')
        else:
            flash('Статья добавлена успешно', category='success')
    return render_template('add_post.html', menu=dbase.getMenu(), title="Добавление статьи")


@app.route("/add_tech", methods= ["POST", "GET"])
@login_required
def addTech():
    if request.method == "POST" and int(current_user.get_admin()) == 1:
        res = dbase.addTech(request.form['summary'], request.form['content'])
        if not res:
            flash('Ошибка добавления статьи', category= 'error')
        else:
            flash('Статья добавлена успешно', category='success')
    return render_template('add_post.html', menu=dbase.getMenu(), title="Добавление статьи")


@app.route('/register', methods=['POST', 'GET'])
@login_required
def register():
    tmp = None
    if request.method == "POST" and int(current_user.get_admin()) == 1:
        if request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(request.form['name'], request.form['email'], hash)
            if res:
                tmp = 'register.html'
                return redirect(url_for('login'))
    else:
        tmp = 'error_admin.html'

    return render_template(tmp)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            userLogin = UserLogin().create(user)
            login_user(userLogin)
            return redirect(url_for('profile')) 
        elif not user:
            flash('Пользователь не найден', category='error')      
    return render_template("login.html", menu=dbase.getMenu())


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile', methods= ["POST", "GET"])
@login_required
def profile():
    data = None
    if int(current_user.get_admin()) == 1:
        data = dbase.getJSON()
        if request.method == "POST":
            res = dbase.updateStatus(request.form['title'], request.form['content'], request.form['status'], request.form['id'])
            if not res:
                flash('Ошибка обновления статуса', category= 'error')
            else:
                flash('Статус успешно обновлен', category='success')
    else:
        data = dbase.getUserPostsJSON(current_user.get_id())
    
    return render_template(
        "admin_panel.html", 
        posts=data, 
        user_name=current_user.get_name(),
        is_admin=int(current_user.get_admin()))

""" @app.route('/image')
def image():
    img = current_user.getAvatar(app)
    if not img:
        return ""
    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h """

if __name__ == "__main__":
    app.run(debug=True) 

