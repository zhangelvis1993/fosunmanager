from dataweb.main import main
from flask import render_template, request, session, redirect, flash
from dataweb.database import *
from dataweb import loginmanager
from flask_login import login_required, login_user, logout_user

@loginmanager.user_loader
def load_user(id):
    return Admin.query.get(int(id))

@main.route('/', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_name = request.form.get('username')
        admin_password = request.form.get('password')
        admin = Admin.query.filter(Admin.ad_name == admin_name, Admin.ad_secret == admin_password).first()
        if admin:
            user = admin.ad_name
            session['log_in'] = user
            login_user(admin, True)
            return redirect('/admin/Charts')
        else:
            flash('用户或密码错误')
            return redirect('/')
    else:
        return render_template('main/login.html')

@main.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')