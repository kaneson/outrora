from . import home
from flask import render_template, flash, redirect, url_for, session
from flask_login import current_user
from ...form import TodoForm
from ...models import Todo
from ... import db

@home.route('/', methods=['GET', 'POST'])
def index():
    form = TodoForm()
    todos = None

    if current_user.is_authenticated:
        todos = Todo.query.filter_by(user_id=current_user.id).all()

    if form.validate_on_submit():
        todo = Todo.query.filter_by(title=form.title.data).first()
        session.pop('message', None)

        if todo is None:            
            t = Todo()
            t.title = form.title.data
            t.user_id = current_user.id
            
            db.session.add(t)
            db.session.commit()
            flash('Task added successfully!')
            flash('success')
            return redirect(url_for('.index'))
        else:
            flash('Task already exist!')
            flash('error')
            return redirect(url_for('.index'))
        
    return render_template('home/index.html', form=form, todos=todos)

@home.route('/task/delete/<int:id>')
def delete_task(id):
    todo = Todo.query.filter_by(id=id).first()
    
    if todo is not None:
        db.session.delete(todo)
        db.session.commit()
        flash('Task removed successfully!')
        flash('success')
    
    flash('Task is not removed')
    flash('error')

    return redirect(url_for('.index'))