from flask import render_template, redirect, url_for, request, flash
from flask_login import logout_user, login_required, login_user
from . import auth
from ...form import LoginForm, RegisterForm
from ...models import User, Todo
from ... import db


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            next = request.args.get('next')

            if next is None or not next.startswith('/'):
                next = url_for('home.index')
            
            return redirect(next)

        flash('You can\'t be logged in system')
        flash('Your e-mail or password is invalid')

    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    print('hello')
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(user)
        if user is None:
            u = User()
            u.name = form.name.data
            u.email = form.email.data
            u.password = form.password.data
            print(u)

            db.session.add(u)
            db.session.commit()
            flash('You were successfully registered')
            flash('success')
            return redirect(url_for('auth.login'))
        else:
            flash('User already registered')
            flash('error')

    return render_template('auth/register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você está sendo logado com sucesso!')
    return redirect(url_for('auth.login'))