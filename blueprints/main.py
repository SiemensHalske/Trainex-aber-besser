from flask import Blueprint, Flask, redirect, render_template, abort, url_for
from jinja2 import TemplateNotFound
import requests
import sqlite3

class Data:
    database_path = 'C:\\Users\\Hendrik\\Documents\\Github\\Trainex aber besser\\database\\users.db'
    
class DataHandler:
    def __init__(self):
        self.database_path = Data.database_path
        self.con = self._get_con()
        
    def _get_con(self):
        con = sqlite3.connect(self.database_path)
        return con
    
    def _get_cursor(self):
        cursor = self.con.cursor()
        return cursor
    
    def _execute(self, query, values):
        cursor = self._get_cursor()
        cursor.execute(query, values)
        self.con.commit()
        cursor.close()
        
    def login_routine(self, username, password):
        username_db, password_db = self.get_credentials_from_db(username, "trainex")
        if username == username_db and password == password_db:
            return True
        else:
            return False
        

url_dict = {
    'index': 'index.html',
    'login': 'login.html',
}

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    # Redirect to url 'auth.login'

    # r = requests.get('http://localhost:5000/auth/login')
    # print(r.status_code)
    # print(r.headers['content-type'])
    # print(r.encoding)
    # print(r.text)
    return redirect(url_for('auth.login'))


@main_bp.route('/<page>', methods=['GET', 'POST'])
def show(page):
    try:
        return render_template('%s.html' % page)
    except TemplateNotFound:
        abort(404)
        
@main_bp.route('/login_page', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@main_bp.route('/login_success', methods=['GET', 'POST'])
def login_success():
    return render_template('index.html')

@main_bp.route('/get_banner', methods=['GET'])
def get_banner():
    return render_template('banner.html')

# in your main.py or wherever you have your route definitions
@main_bp.route('/banner', methods=['GET'])
def banner():
    return render_template('banner.html')


@main_bp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404