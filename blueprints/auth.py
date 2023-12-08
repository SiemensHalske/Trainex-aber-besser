from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from forms.login_form import LoginForm
from models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print(f"Form: {form}")  # Debug print
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.login_success'))
        flash('Invalid username or password')
    print(form.errors)
    print(form.username.data)
    print("Test")
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
