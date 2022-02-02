from crypt import methods
from models import Users, Items, Feedback
from init import app
from flask import make_response, redirect, render_template,\
    escape, abort, request, session, url_for, flash
from datetime import datetime, timedelta
import sqlalchemy
# //app.register_error_handler('404.html', page_not_found)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/login', methods=['GET', 'POST'])
def login():
    resp = make_response(render_template('login.html'))
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        try:
            if Users.query.filter_by(name=name).one().validate(password):
                session['name'] = name
                flash(f'Welcome back, {name}', 'success')
                return redirect(url_for('index'), code=301)
            flash('Wrong login or password', 'warning')
        except sqlalchemy.exc.NoResultFound:
            flash('Wrong login or password', 'danger')
        finally:
            resp.status_code = 401
    return resp

@app.route('/logout')
def logout():
    if session.get('name'):
        session.pop('name')
    return redirect('/', code=302)

@app.route('/<name>')
def profile(name):
    if session.get('name') == name:
        if Users.query.filter_by(name=name) is not None:
            return f'Hello, {escape(name)}'
    flash('Please authenticate', 'warning')
    return redirect(url_for('login'), code=301)

@app.route('/')
def index():
    resp = make_response(render_template('index.html'))
    print(request.cookies.get('test'))
    if not request.cookies.get('test'):
       resp.set_cookie('test', 'testvalue', expires=datetime.now()+timedelta(minutes=30))
    return resp

@app.route('/about', methods=['GET', 'POST'])
def about():
    feedback = Feedback.query.all()
    if request.method == 'POST':
        login = request.form.get('login')
        text = request.form.get('text')
        if login != '' and text != '':
            f = Feedback(name=login, text=text)
            db.session.add(f)
            db.session.commit()
            feedback.append(f)
    print(feedback)
    return render_template('about.html', feedback=feedback)

@app.route('/catalog')
def catalog():
    min_price = int(request.args.get('min_price', 0))
    max_price = int(request.args.get('max_price', 10e9))
    items = Items.query.all()
    items = list(filter(lambda x: min_price <= x.price <= max_price, items))
    return render_template('catalog.html', items=items)

@app.route('/item/<item>')
def show_item_profile(item):
    item = escape(item)
    return render_template('item.html', item=Items.query.filter_by(name=item).one())
    return abort(404, description="not found")

if __name__ == '__main__':
    app.run(debug=True)