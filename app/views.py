from flask import render_template, flash, request, abort, redirect, url_for
from flask_admin.helpers import is_safe_url
from flask_login import login_user
from flask_security import LoginForm
from sqlalchemy.sql.functions import user

from app import app, db


@app.route('/')
@app.route('/base/')
def base():
    return render_template('base.html')


@app.route('/menu/')
def menu():
    return render_template('menu.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flash('Logged in successfully.')

        next = request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return abort(400)

        return redirect(next or url_for('base'))
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)


# pip install flask_sqlalchemy
# в python консоли
# from app import app, db
# app.app_context().push()
# db.create_all()







