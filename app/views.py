from flask import render_template, flash, request, abort, redirect, url_for, current_app
from flask_admin.helpers import is_safe_url
from flask_login import login_user, current_user, login_required, logout_user, LoginManager
from flask_security.core import AnonymousUser
from sqlalchemy import insert

from app.forms import LoginForm
from werkzeug.security import generate_password_hash

from app import app, db
from app.models import User, Menu, Order, OrderIn

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
    messages =''
    print('tyt')
    if request.method == 'POST':
        print('tyt2')
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        print('tyt3')
        hash_password = generate_password_hash(password)
        user_exist_username = User.query.filter_by(username=username).first()
        print('user_exist_username', user_exist_username)
        user_exist_email = User.query.filter_by(email=email).first()
        print('user_exist_email', user_exist_email)
        if user_exist_username:
            messages = 'Логин занят, придумайте другой'
            print(messages)
        elif user_exist_email:
            messages = 'Пользователь с данным email уже зарегистрирован'
            print(messages)
        else:
            user = User(name=name
                        , username=username
                        , email=email
                        , password=hash_password)
            try:
                print('тут')
                db.session.add(user)
                db.session.commit()
                messages = f'Успешная регистрация (пользователь: {name})'
                print(messages)
                return render_template('register.html', current_user=current_user, messages=messages)
            except:
                messages = "При добавлении пользователя произошла ошибка"
                print(messages)
                return render_template('register.html', current_user=current_user, messages=messages)
        return render_template('register.html', current_user=current_user, messages=messages)
    else:
        print('esleend')
        return render_template('register.html', current_user=current_user, messages=messages)


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
            menu_id = int(request.form.get('menu.id'))
            if menu_id in basket_list:
                basket_list[menu_id] += 1
            else:
                basket_list.update({menu_id: 1})
        if 'del' in request.form:
            menu_id = int(request.form.get('menu.id'))
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
    for i in basket_list:
        menu = Menu.query.filter_by(id=i).first()
        name = menu.name_food
        price = menu.price
        amount = basket_list[i]
        list_info.update(
            {i: f"{name}, количество = {amount}, сумма: {float(price)} руб. * {amount} = {float(price) * amount} руб."})
        res += price * amount
    if request.method == 'POST':
        if 'add' in request.form:
            menu_id = int(request.form.get('key'))
            if menu_id in basket_list:
                basket_list[menu_id] += 1
            else:
                basket_list.update({menu_id: 1})
        if 'del' in request.form:
            menu_id = int(request.form.get('key'))
            if menu_id in basket_list:
                if basket_list[menu_id] > 1:
                    basket_list[menu_id] -= 1
                elif basket_list[menu_id] == 1:
                    basket_list.pop(menu_id)
        if 'order' in request.form:
            if current_user.id > 1:
                user_id = current_user.id
                deli = request.form.get('deli')
                phone = request.form.get('phone')
                address = request.form.get('address')
                comment = request.form.get('comment')
                delivery = 'self'
                if deli == 'avto':
                    res += 200
                    delivery = 'avto'
                order = Order(user_id=user_id
                              , summa=res
                              , delivery=delivery
                              , phone=phone
                              , address=address
                              , comment=comment)
                try:
                    db.session.add(order)
                    db.session.commit()
                except:
                    return "При добавлении заказа произошла ошибка"
                number = Order.query.order_by(Order.id.desc()).first()
                for i in basket_list:
                    menu = Menu.query.filter_by(id=i).first()
                    price = menu.price
                    count = int(basket_list[i])
                    summa = price * count
                    orderin = OrderIn(order_id=number.id,
                                      menu_id=i,
                                      count=count,
                                      summa=summa)
                    try:
                        db.session.add(orderin)
                        db.session.commit()
                    except:
                        return "При добавлении заказа произошла ошибка"
                basket_list.clear()
                list_info.clear()
                messages = f'Заказ создан, номер {number.id}'
            else:
                messages = 'Для оформления заказа нужно авторизоваться'
    title = 'Корзина'
    return render_template('basket.html', current_user=current_user, list_info=list_info, title=title
                           , res=res, messages=messages)


@app.route('/orders/')
def orders():
    global current_user
    orderss = Order.query.filter_by(user_id=current_user.id).order_by(Order.id.desc()).all()
    title = 'Заказы'
    return render_template('orders.html', current_user=current_user, title=title, orderss=orderss)
















if __name__ == '__main__':
    app.run(debug=True)


# pip install flask_sqlalchemy
# в python консоли
# from app import app, db
# app.app_context().push()
# db.create_all()







