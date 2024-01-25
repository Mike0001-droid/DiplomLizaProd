import sqlite3, os
from flask import Flask, render_template, request, url_for, flash, redirect, g
from DataBase import DataBase
from flask_login import LoginManager, login_user, login_required
from UserLogin import UserLogin
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = '/tmp/database.db'
DEBUG = True
SECRET_KEY = 'gadsgsf123&81230><asd,'
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
    print("load_user")
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
        return render_template('index.html', posts=dbase.getJSON(), path=path, path1=path1, path2=path2, path3=path3)


@login_required
@app.route("/update_status", methods= ["POST", "GET"])
def updateStatus():
    if request.method == "POST":
        res = dbase.updateStatus(request.form['title'], request.form['content'], request.form['status'], request.form['id'])
        if not res:
            flash('Ошибка обновления статуса', category= 'error')
        else:
            flash('Статус успешно обновлен', category='success')
    else:
        flash('Ошибка обновления статуса', category='error')
    return render_template('admin.html', menu=dbase.getJSON())


@login_required
@app.route("/add_post", methods= ["POST", "GET"])
def addPost():
    if request.method == "POST":
        res = dbase.addPost(request.form['title'], request.form['content'])
        if not res:
            flash('Ошибка добавления статьи', category= 'error')
        else:
            flash('Статья добавлена успешно', category='success')
        
    return render_template('add_post.html', menu=dbase.getMenu(), title="Добавление статьи")



@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        if request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(request.form['name'], request.form['email'], hash)
            if res:
                return redirect(url_for('login'))
    return render_template('register.html', menu=dbase.getMenu())



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            userLogin = UserLogin().create(user)
            login_user(userLogin)
            return redirect(url_for('index'))           
    return render_template("login.html", menu=dbase.getMenu())



""" 
@app.route('/successfulauth', methods=['GET', 'POST'])
def successfulauth():
        conn = connect_db()
        cursor_db = conn.cursor()
        posts = conn.execute('SELECT * FROM user').fetchall()
        id = cursor_db.execute("SELECT fio FROM user where login = ?", (LOG, )).fetchone()[0]
        gruppa = cursor_db.execute("SELECT gruppa FROM user where login = ?", (LOG, )).fetchone()[0]
        
        cursor_db.close()
        conn.close()
        return render_template('successfulauth.html', LOG=LOG, id=id,gruppa=gruppa,posts=posts)


@app.route("/contact", methods=["POST","GET"])
def contact():
         if request.method == 'POST':
                print(request.form)
                return render_template('contact.html', title = "обратная")
if __name__ == "__main__":
    app.run(debug=True) """
if __name__ == "__main__":
    app.run(debug=True)