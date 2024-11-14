from flask import render_template, flash, request, abort, redirect, url_for, current_app
from flask_admin.helpers import is_safe_url
from flask_login import login_user, current_user, login_required, logout_user, LoginManager
from flask_security.core import AnonymousUser

from app.forms import LoginForm
from werkzeug.security import generate_password_hash

from app import app, db
from app.models import User, Menu

app.config['SECRET_KEY'] = 'any secret string'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

basket_list = {}


@app.route('/')
@app.route('/base/')
def base():
    global current_user
    return render_template('base.html', current_user=current_user)


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


@app.route('/logout/')
def logout():
    global current_user
    current_user = User.query.filter_by(id=1).first()
    messages = 'Вы вышли из личного кабинета'
    form = LoginForm()
    return render_template('login.html', form=form, messages=messages, current_user=current_user)


@app.route('/menu/', methods=['GET', 'POST'])
def menu():
    global current_user, basket_list
    if request.method == 'POST':
        if 'add' in request.form:
            form_dict = dict(request.form)
            menu_id = int(form_dict['menu.id'])
            if menu_id in basket_list:
                basket_list[menu_id] += 1
            else:
                basket_list.update({menu_id: 1})
        if 'del' in request.form:
            form_dict = dict(request.form)
            menu_id = int(form_dict['menu.id'])
            if menu_id in basket_list:
                if basket_list[menu_id] > 1:
                    basket_list[menu_id] -= 1
                elif basket_list[menu_id] == 1:
                    basket_list.pop(menu_id)
    menus = Menu.query.all()
    return render_template('menu.html', current_user=current_user, menus=menus
                           , basket_list=basket_list)


@app.route('/basket/', methods=['GET', 'POST'])
def basket():
    global current_user, basket_list
    list_info = {}
    res = 0
    messages = ''
    if request.method == 'POST':
        if 'add' in request.form:
            form_dict = dict(request.form)
            menu_id = int(form_dict['key'])
            if menu_id in basket_list:
                basket_list[menu_id] += 1
            else:
                basket_list.update({menu_id: 1})
        if 'del' in request.form:
            form_dict = dict(request.form)
            menu_id = int(form_dict['key'])
            if menu_id in basket_list:
                if basket_list[menu_id] > 1:
                    basket_list[menu_id] -= 1
                elif basket_list[menu_id] == 1:
                    basket_list.pop(menu_id)
    for i in basket_list:
        menu = Menu.query.filter_by(id=i).first()
        name = menu.name_food
        price = menu.price
        amount = basket_list[i]
        list_info.update(
            {i: f"{name}, количество = {amount}, сумма: {float(price)} руб. * {amount} = {float(price) * amount} руб."})
        res += price * amount
    title = 'Корзина'
    return render_template('basket.html', current_user=current_user, list_info=list_info, title=title
                           , res=res, messages=messages)



















if __name__ == '__main__':
    app.run(debug=True)


# pip install flask_sqlalchemy
# в python консоли
# from app import app, db
# app.app_context().push()
# db.create_all()







