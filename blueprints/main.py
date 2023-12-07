from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/index')
def index2():
    return render_template('index.html')

@main_bp.route('/<page>')
def show(page):
    try:
        return render_template('%s.html' % page)
    except TemplateNotFound:
        abort(404)
        
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@main_bp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
