from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user

from blog.forms import LoginForm
from blog.models import Admin
from blog.utils import redirect_back

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.first()
        if admin:
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember)
                flash('登陆成功！', 'info')
                return redirect_back()
            flash('账号或密码错误！','warning')
        else:
            flash('该账号尚未注册，请检查后重新输入！', 'warning')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('已退出登陆！', 'info')
    return redirect_back()
