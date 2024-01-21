import sqlite3 
from flask import Flask, render_template, request, url_for, flash, redirect, g
from werkzeug.exceptions import abort
from flask import Flask,  render_template
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
LOG=""

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    db = get_db_connection()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = get_db_connection()
    return g.link_db

dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db) 


@app.teardown_appcontext
def close_db():
    if hasattr(g, 'link_db'):
        g.link_db.close()


