from flask import render_template, flash, request, abort, redirect, url_for, current_app
from flask_admin.helpers import is_safe_url
from flask_login import login_user, current_user, login_required, logout_user, LoginManager
from flask_security.core import AnonymousUser

from app.forms import LoginForm
from werkzeug.security import generate_password_hash

from app import app, db
from app.models import User

app.config['SECRET_KEY'] = 'any secret string'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route('/')
@app.route('/base/')
def base():
    global current_user
    return render_template('base.html', current_user=current_user)


@app.route('/menu/')
def menu():
    global current_user
    return render_template('menu.html', current_user=current_user)


@app.route('/register/', methods=['POST', 'GET'])
def register():
    global current_user
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        hash_password = generate_password_hash(password)

        user = User(name=name
                    , username=username
                    , email=email
                    , password=hash_password)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/')
        except:
            return "При добавлении пользователя произошла ошибка"
    else:
        return render_template('register.html', current_user=current_user)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    global current_user
    print('current_user', current_user)
    messages = ''
    form = LoginForm()
    if form.validate_on_submit():
        # Validate the user's credentials
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(str(request.form['password'])):
            current_user = user
            return redirect('/')
        messages = 'Некорректный логин или пароль'
    return render_template('login.html', form=form, messages=messages, current_user=current_user)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()    # Fetch the user from the database


if __name__ == '__main__':
    app.run(debug=True)


# pip install flask_sqlalchemy
# в python консоли
# from app import app, db
# app.app_context().push()
# db.create_all()







