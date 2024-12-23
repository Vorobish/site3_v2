from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    '''
        Класс пользователь
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    # Нужен для security!
    active = db.Column(db.Boolean())

    # Flask - Login
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Menu(db.Model):
    '''
        Меню - товар в меню
    '''
    id = db.Column(db.Integer, primary_key=True)
    name_food = db.Column(db.String(30), nullable=False)
    category = db.Column(db.Integer, nullable=False)
    weight_gr = db.Column(db.Integer)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    ingredients = db.Column(db.Text)
    image = db.Column(db.String(30))
    time_create = db.Column(db.DateTime)
    time_update = db.Column(db.DateTime)


class Order(db.Model):
    '''
        Заказ
    '''
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer)
    summa = db.Column(db.Numeric(10, 2), nullable=False)
    delivery = db.Column(db.String, default='self')
    phone = db.Column(db.String)
    address = db.Column(db.String)
    pay_stat = db.Column(db.String, default='not')
    status = db.Column(db.Integer, default=1)
    comment = db.Column(db.Text)
    time_create = db.Column(db.DateTime, default=datetime.now())
    time_update = db.Column(db.DateTime, default=datetime.now())


class OrderIn(db.Model):
    '''
        Состав заказа
    '''
    __tablename__ = 'orderins'
    id = db.Column(db.Integer, primary_key=True, index=True)
    order_id = db.Column(db.Integer, nullable=False, index=True)
    menu_id = db.Column(db.Integer, nullable=False, index=True)
    count = db.Column(db.Integer)
    summa = db.Column(db.Numeric(10, 2))
    time_create = db.Column(db.DateTime, default=datetime.now())
    time_update = db.Column(db.DateTime, default=datetime.now())

# flask db init
# flask db migrate -m "Initial migration."
# flask db upgrade
# flask db migrate -m "Initial revision."
# flask db upgrade
