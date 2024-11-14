from flask import render_template
from app import app, db


@app.route('/')
@app.route('/base/')
def base():
    return render_template('base.html')


@app.route('/menu/')
def menu():
    return render_template('menu.html')


if __name__ == '__main__':
    app.run(debug=True)


# pip install flask_sqlalchemy
# в python консоли
# from app import app, db
# app.app_context().push()
# db.create_all()







