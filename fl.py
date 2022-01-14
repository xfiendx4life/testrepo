from flask import Flask, redirect, render_template, escape, url_for, abort

app = Flask(__name__)
# app.register_error_handler('404.html', page_not_found)

class Items:
    def __init__(self, name='item', descr='some description', price='300$') -> None:
        self.name = name
        self.descr = descr
        self.price = price

ITEMS = [Items('Alexei', 'Kaput', '1945'), Items(),\
    Items('panther', "the most beautiful panther eva", "400$")]

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/catalog')
def catalog():
    return render_template('catalog.html', items=ITEMS)

@app.route('/item/<item>')
def show_item_profile(item):
    # show the user profile for that user
    for thing in ITEMS:
        if thing.name == item:
            return render_template('item.html', item=thing)
    return abort(404, description="not found")

if __name__ == '__main__':
    app.run(debug=True)