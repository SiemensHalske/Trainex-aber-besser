from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
